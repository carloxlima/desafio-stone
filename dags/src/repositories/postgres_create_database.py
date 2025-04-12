from abc import ABC, abstractmethod
from src.interfaces.interface_database import InterfaceDatabase
from airflow.providers.postgres.hooks.postgres import PostgresHook
import polars as pl
from psycopg2 import sql

class PostgresCreateDatabase (InterfaceDatabase):
    """
    Class to create a PostgreSQL database.
    This class is used to create a new database in PostgreSQL.
    """
    
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
    
    def _verify_database(self):
        """
        Verify if the database exists in PostgreSQL.
        
        :param database_name: The name of the database to verify.
        :return: True if the database exists, False otherwise.
        """
        # Use the engine to execute the SQL command to check if the database exists
        with self.engine.connect() as connection:
            result = connection.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.database_name}'")
            return result.fetchone() is not None
        
    def create_database(self, database_name: str):
        """
        Create a new database in PostgreSQL.
        
        :param database_name: The name of the database to create.
        """
        
        self.database_name = database_name

        if self._verify_database():
            print(f"Database {database_name} already exists.")
            return
        else:
            print(f"Creating database {database_name}...")
            with self.engine.connect() as connection:
                connection.execution_options(isolation_level="AUTOCOMMIT").execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier('dbpedrapagamentos'))
    )
            print(f"Database {database_name} created successfully.")
            # Close the connection
            self.engine.dispose()
    
    def insert_dataframe(self, df: pl.DataFrame, table_name: str):
        pass