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
    def __init__(self, db_writer):
        """
        Initialize the BucketFileService class.
        :param db_writer: The database writer to be used to insert the files into the database.
        """
        self.url = ''
        self.db_writer = db_writer

    def _reader_files_parquet(self, link_bucket: str):
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
    

    def get_file_hash(df: pl.DataFrame, algo: str = 'sha256') -> str:
        """
        Calculate the hash of the dataframe.
        The hash is calculated using the specified algorithm.
        The default algorithm is sha256.
        :param df: The dataframe to be hashed.
        :param algo: The algorithm to be used to calculate the hash.
        :return: The hash of the dataframe.
        """
        import hashlib
        buffer = io.BytesIO()
        df.write_csv(buffer, include_header=True)
        buffer.seek(0)
        return hashlib.new(algo, buffer.read()).hexdigest()
    
    def insert_file_parquet_from_database(self, url: str, id: str, table_name: str, column_name: str):
        """
        This function verify if the id is unique on the table and insert the dataframe on the database. \n
        The dataframe is inserted on the database using the PostgresHook. \n
        :param url: The url is the link to the file on the bucket.
        :param id: The id to be verified.
        :param table_name: The name of the table to be verified.
        :param column_name: The name of the column to be verified.
        """
        self.url = url
                
        if self.db_writer.verify_unique_id_table(id, table_name, column_name) is None:
            self.db_writer.insert_process_log(file_name=id, process_status='Started')
            self.db_writer.insert_file_parque(self._reader_files_parquet(self.url))
        else: 
            print('File didnt inserted on the database')
        
    
    def insert_database(self, df, table_name):
        """
        Insert the dataframe on the database.
        The dataframe is inserted on the database using the PostgresHook.
        """
        if self.db_writer.verify_unique_id_table():
            self._reader_files_parquet(self.url)
            self.db_writer.insert_dataframe(df, table_name)