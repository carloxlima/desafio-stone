from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from pendulum import datetime
from src.services import BucketFileLoader, BucketFileService
from src.repositories.postgres_writer import PostgresWriter
import polars as pl



@dag(
    dag_id="etl_dag",
    description="DAG to ETL",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"owner": "Carlos", "retries": 0},
    tags=['extractor', 'transformer', 'loader'],
)

def dat_etl():


    with TaskGroup("extractor") as tg_extractor:

        @task
        def load_links():   
            return BucketFileLoader('http://storage.googleapis.com/desafio-eng-dados/').get_files_parquet()
            
        @task
        def load_files(urls):
            
            bucket_file_service = BucketFileService(PostgresWriter(connection="postgres_conn"))
            for url in urls:
                id = url.split('/')[-1]
                df = bucket_file_service.insert_file_parquet_from_database(url=url, id=id, table_name='tb_process_log', column_name='file_name')
                
            
        dados_transformados = load_files(load_links())

    with TaskGroup("transformer") as tg_transformer:
        @task
        def create_db():   
            pass
        
        create_db()

    with TaskGroup("loader") as tg_loader:
        @task
        def create_db():   
            pass
        
        create_db()    
# Instantiate the DAG
dat_etl()