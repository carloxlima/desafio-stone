import polars as pl
import requests
import io
from pathlib import Path


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
        self.db_writer = db_writer
        self.id = ""
        self.project_root = Path(__file__).resolve().parents[3]

    def transformation(self, urls: str):
        """
        This function transforms the files on the bucket and insert them on the database.
        :param urls: The urls to be transformed.
        """

        self.paths = []
        for url in urls:
            id = url.split("/")[-1]
            dfpl = self._reader_files_parquet(url)
            df = dfpl.fill_null("Não Informado")  # para todas as colunas
            df = df.with_columns([pl.lit(id).alias("file_name")])

            df = df.rename(
                {"customer_id": "customer_code", "cancellation_reason": "reason"}
            )

            # Limitação de linhas devido meu computador.
            # df = df.head(500_000)

            output_path = f"/tmp/{id}.parquet"
            df.write_parquet(output_path)
            self.paths.append(output_path)
        return self.paths

    def loader(self, path):
        """
        This function loads the files on the database.
        :param path: The path to the file to be loaded.
        """

        self.id = path.split("/")[-1].replace(".parquet", "")
        if (
            self.db_writer.verify_unique_id_table(
                self.id, table_name="tb_process_log", column_name="file_name"
            )
            is None
        ):
            self.db_writer.insert_all(pl.read_parquet(path))
            self.db_writer.insert_process_log(
                file_name=self.id,
                process_status="Started",
                step=1,
                error_message=None,
                processed=False,
            )

    def _reader_files_parquet(self, link_bucket: str) -> pl.DataFrame:
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
            raise Exception(
                f"Failed to get files from bucket: {response.status_code}")

    def update_process_log(self):
        """
        This function update the process log on the database.
        :param id: The id to be updated.
        :param table_name: The name of the table to be updated.
        :param column_name: The name of the column to be updated.
        """

        self.db_writer.upd_status_log(
            file_name=self.id,
            process_status="Processed",
            error_message=None,
            step=1,
            processed=True,
        )
