from src.interfaces.interface_database import InterfaceDatabase
from airflow.providers.postgres.hooks.postgres import PostgresHook
import polars as pl
from src.models.base import Base


class PostgresCreateTables(InterfaceDatabase):
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
        self.hook = PostgresHook(postgres_conn_id=self.connection)
        engine = self.hook.get_sqlalchemy_engine()
        return engine

    def create_tables(self, file_sql: str = "create_tables.sql"):
        """
        Create the tables in the PostgreSQL database. \n
        This method creates the tables in the PostgreSQL database.\n
        :param file_sql: The path to the SQL file with the commands to create the tables. \n
                         This parameter is optional.

        """
        from pathlib import Path

        project_root = Path(__file__).resolve().parents[3]
        sql_path = project_root / "include" / "sql" / file_sql

        with open(sql_path, "r") as f:
            sql = f.read()
        self.hook.run(sql)

    def insert_dataframe(self, df: pl.DataFrame, table_name: str):
        pass

    def create_tables_models(self):
        Base.metadata.create_all(self.engine)

    def create_dw_tables(self, file_sql: str = "create_tables_dw.sql"):
        from pathlib import Path

        project_root = Path(__file__).resolve().parents[3]
        sql_path = project_root / "include" / "sql" / file_sql

        with open(sql_path, "r") as f:
            sql = f.read()
        self.hook.run(sql)
