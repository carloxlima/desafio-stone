import polars as pl
from sqlalchemy import create_engine
from src.interfaces.interface_database import InterfaceDatabase
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresWriter(InterfaceDatabase):
    
    def __init__(self, connection: str):
        """
        Initialize the PostgreDatabase class.
        
        :param connection_string: The connection string to connect to the PostgreSQL database.
        Connection configured on Airflow UI.
        This connection used on PostgresHook.
        """
        self.connection = connection
        self.engine = self._create_connection()

    def _create_connection(self):
        self.hook = PostgresHook(postgres_conn_id=self.connection)
        engine = self.hook.get_sqlalchemy_engine()
        return engine


    def verify_unique_id_table(self, id: str, table_name: str, column_name: str):
        """
        Verify if the id is unique on the table.            
        :param id: The id to be verified.
        :param table_name: The name of the table to be verified.
        :param column_name: The name of the column to be verified.
        :return: True if the id is unique, False otherwise.
        """
        sql = f"""
            SELECT 1 FROM public.{table_name}
            WHERE {column_name} = %(file_name)s
            LIMIT 1;
            """

        return  self.hook.get_first(sql, parameters={"file_name": id})
    
    def verify_unique_id_hash_table(self, hash: str, id: str, table_name: str, column_name: str):
        """
        Verify if the id is unique on the table.            
        The hash is used to verify if the file is already inserted on the database.
        :param hash: The hash of the file to be verified.
        :param id: The id to be verified.
        :param table_name: The name of the table to be verified.
        :param column_name: The name of the column to be verified.
        :return: True if the id is unique, False otherwise.
        """
        return self.hook.run(f"SELECT * FROM public.{table_name} where {column_name} = '{id}' and file_hash ='{hash}' limit 1;")
        

    def insert_dataframe(self, df: pl.dataframe, table_name: str):
        """
        Insert the dataframe on the database.           
        The dataframe is inserted on the database using the PostgresHook.
        """
        df = df.to_pandas()
        
        df.to_sql(table_name, con=self.engine, if_exists='append', index=False)    
    
    def insert_process_log(self, file_name: str, process_status: str):
        """
        Insert the process log on the database.           
        The process log is inserted on the database using the PostgresHook.
        :param file_name: The name of the file to be inserted.
        :param process_status: The status of the process to be inserted.
        :return: True if the process log is inserted, False otherwise.
        """

        sql = """
            INSERT INTO public.tb_process_log(file_name, process_status)
            VALUES (%(file_name)s, %(process_status)s);
            """

        return self.hook.run(sql, parameters={ "file_name": file_name,"process_status": process_status})
    

    def insert_file_parque(self, df: pl.DataFrame):
        """
        Insert the file on the database.
        The file is inserted on the database using the PostgresHook.
        :param df: The dataframe to be inserted.                        
        """
        
        for row in df.iter_rows(named=True):
            
            customer_params = {
                "customer_phone": row['customer_phone']
            }
            
            customer_sql = """
            INSERT INTO public.tb_customers (customer_phone, customer_email)
            VALUES (%(customer_phone)s)
            RETURNING customer_id;
            """
            
            customer_id = self.hook.get_first(customer_sql, parameters=customer_params)[0]

            # Inserir dados na tabela addresses
            address_params = {
                "customer_id": customer_id,
                "city": row['city'],
                "country": row['country'],
                "country_state": row['country_state'],
                "zip_code": row['zip_code'],
                "street_name": row['street_name'],
                "neighborhood": row['neighborhood'],
                "complement": row['complement']
            }
            
            address_sql = """
            INSERT INTO public.tb_addresses (customer_id, city, country, country_state, zip_code, street_name, neighborhood, complement)
            VALUES (%(customer_id)s, %(city)s, %(country)s, %(country_state)s, %(zip_code)s, %(street_name)s, %(neighborhood)s, %(complement)s)
            RETURNING address_id;
            """
            
            address_id = self.hook.get_first(address_sql, parameters=address_params)[0]

             
            cancellation_reason_sql = """
                INSERT INTO public.tb_cancellation_reasons (reason)
                VALUES (%(reason)s)
                RETURNING id;
            """
            cancellation_reason_id = self.hook.get_first(cancellation_reason_sql, parameters={"reason": row['cancellation_reason']})[0]

            # Inserir dados na tabela orders
            order_params = {
                "order_number": row['order_number'],
                "provider": row['provider'],
                "technician_email": row['technician_email'],
                "cancellation_reason_id": cancellation_reason_id,  # Isso pode ser mapeado para uma ID
                "arrival_date": row['arrival_date'],
                "deadline_date": row['deadline_date'],
                "last_modified_date": row['last_modified_date']
            }
            
            order_sql = """
            INSERT INTO public.tb_orders (order_number, provider, technician_email, cancellation_reason_id, arrival_date, deadline_date, last_modified_date)
            VALUES (%(order_number)s, %(provider)s, %(technician_email)s, %(cancellation_reason_id)s, %(arrival_date)s, %(deadline_date)s, %(last_modified_date)s)
            """
            
            self.hook.run(order_sql, parameters=order_params)



        