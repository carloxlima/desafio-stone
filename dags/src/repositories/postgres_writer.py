import polars as pl
from sqlalchemy import create_engine
from src.interfaces.interface_database import InterfaceDatabase
from airflow.providers.postgres.hooks.postgres import PostgresHook
from src.interfaces.session_manager import SessionManager
from sqlalchemy import update
from datetime import datetime
from src.models import Customer
from src.models import Address
from src.models import CancellationReason
from src.models import Order
from src.models import ProcessLog





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

        with SessionManager() as session:   
            self.session = session

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

    def insert_process_log(self, file_name: str, process_status: str, step: int, error_message: str = None, processed: bool = False):
        new_log = ProcessLog(
            file_name=file_name,
            process_status=process_status,
            process_time=datetime.now(),
            error_message=error_message,
            processed=processed,
            step=step
        )
        self.session.add(new_log)
        self.session.commit() 
    
    # def insert_process_log(self, file_name: str, process_status: str):
    #     """
    #     Insert the process log on the database.           
    #     The process log is inserted on the database using the PostgresHook.
    #     :param file_name: The name of the file to be inserted.
    #     :param process_status: The status of the process to be inserted.
    #     :return: True if the process log is inserted, False otherwise.
    #     """

    #     sql = """
    #         INSERT INTO public.tb_process_log(file_name, process_status, step)
    #         VALUES (%(file_name)s, %(process_status)s, %(step)s);
    #         """

    #     return self.hook.run(sql, parameters={ "file_name": file_name,"process_status": process_status, "step": 1 })
    
    def insert_all(self, df: pl.DataFrame):
        # De-duplicar
        customer_data = df.select(["customer_phone","customer_code"]).unique().to_dicts()
        address_data = df.select([
            "customer_code", "city", "country", "country_state", "zip_code", 
            "street_name", "neighborhood", "complement"
        ]).to_dicts()
        cancellation_data = df.select(["reason"]).unique().to_dicts()
        order_data = df.to_dicts()

        with SessionManager() as session:
            # Insert Customers
            session.bulk_insert_mappings(Customer, customer_data)
            session.flush()  # Garantir que customer_id seja populado

            customer_map = {
                c.customer_code: c.customer_id
                for c in session.query(Customer).all()
            }
            #print(f'customer_map: {customer_map}')

            # Insert Cancellation Reasons
            session.bulk_insert_mappings(CancellationReason, cancellation_data)
            session.flush()

            reason_map = {
                r.reason: r.id
                for r in session.query(CancellationReason).all()
            }

            # Insert Addresses
            address_records = []
            for addr in address_data:
                #print(f'customer_map: {addr["customer_code"]}')
                address_records.append({
                    "customer_id": customer_map.get(addr["customer_code"]),
                    **{k: addr[k] for k in addr if k != "customer_code"}
                })
            session.bulk_insert_mappings(Address, address_records)

            # Insert Orders
            order_records = []
            for row in order_data:
                order_records.append({
                    "order_number": row["order_number"],
                    "provider": row["provider"],
                    "technician_email": row["technician_email"],
                    "cancellation_reason_id": reason_map.get(row["reason"]),
                    "customer_id": customer_map.get(addr["customer_code"]),
                    "arrival_date": row["arrival_date"],
                    "deadline_date": row["deadline_date"],
                    "last_modified_date": row["last_modified_date"],
                    "terminal_serial_number":row["terminal_serial_number"], 
                    "terminal_model":row["terminal_model"], 
                    "terminal_type": row["terminal_type"],
                    "file_name": row["file_name"]
                })
            session.bulk_insert_mappings(Order, order_records)


    def upd_status_log( self, file_name: str,  process_status: str, step: int, error_message: str = None, processed: bool = False):
        stmt = (
            update(ProcessLog)
            .where(ProcessLog.file_name == file_name)
            .values(
                process_status=process_status,
                process_time=datetime.now(),
                error_message=error_message,
                processed=processed,
                step=step
            )
        )

        self.session.execute(stmt)
        self.session.commit()