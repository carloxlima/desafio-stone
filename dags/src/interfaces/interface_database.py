from abc import ABC, abstractmethod
import polars as pl

class InterfaceDatabase(ABC):
    """
    Interface for database operations.
    """
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