from abc import ABC, abstractmethod
import polars as pl

class InterfaceDatabase(ABC):
    """
    Interface for database operations.
    """

    @abstractmethod
    def insert_dataframe(self, df: pl.dataframe, table_name: str):
        """
        Write a DataFrame to the database.
        :param df: The DataFrame to write.
        :param table_name: The name of the table to write to.   
        """
        pass
    
    @abstractmethod
    def _create_connection(self):
        """
        Create a connection to the database.
        :return: A connection object.
        """
        pass

    # @abstractmethod
    # def disconnect(self):
    #     """
    #     Disconnect from the database.
    #     """
    #     pass

    # @abstractmethod
    # def execute_query(self, query: str):
    #     """
    #     Execute a query on the database.

    #     :param query: The SQL query to execute.
    #     :return: The result of the query.
    #     """
    #     pass