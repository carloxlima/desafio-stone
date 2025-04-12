import polaris as pl
from sqlalchemy import create_engine
from interfaces.interface_database import InterfaceDatabase
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresWriter(InterfaceDatabase):
    
    def __init__(self, connection: str):
        """
        Initialize the PostgreDatabase class.
        
        :param connection_string: The connection string to connect to the PostgreSQL database.
        """
        self.connection = connection
        self.engine = self._create_connection()

    def _create_connection(self):
        hook = PostgresHook(postgres_conn_id=self.connection)
        engine = hook.get_sqlalchemy_engine()
        return engine

    def insert_dataframe(self, df: pl.dataframe, table_name: str):
        df.to_sql(table_name, con=self.engine, if_exists='append', index=False)    