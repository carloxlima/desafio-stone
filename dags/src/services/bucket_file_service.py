import polars as pl
import requests
import io

class BucketFileService:
    """
    Class to read files on the bucket and insert on the database.
    This class is used to read files from the bucket and insert them into the database.
    The files are in parquet format.
    The class uses the polars library to read the files.

    """
    def __init__(self, url : list, db_writer):
        self.url = url

    def _reader_files_parquet(self, link_bucket):
        """
        Read the files from the bucket and load on the dataframe polars.
        Return a dataframe polars with the files.
        """
        response = requests.get(link_bucket)

        if response.status_code == 200:
            response.raise_for_status()
            df = pl.read_parquet(io.BytesIO(response.content))
            return df
        else:
            raise Exception(f"Failed to get files from bucket: {response.status_code}")
        
    def insert_database(self, df, table_name):
        """
        Insert the dataframe on the database.
        The dataframe is inserted on the database using the PostgresHook.
        """
        self._reader_files_parquet(self.url)
        self.db_writer.insert_dataframe(df, table_name)