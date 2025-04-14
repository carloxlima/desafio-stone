from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from pendulum import datetime
from src.services import BucketFileLoader, BucketFileService, DataWarehouseETL, VerifyProcessLog, ManagerEvidence
from src.repositories import PostgresWriterDw, PostgresWriter, PostgresVerifyLog, PostgresManagerEvidence




@dag(
    dag_id="dag_etl_pedrapagamento",
    description="DAG to ETL",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"owner": "Carlos", "retries": 0},
    tags=['extractor', 'transformer', 'loader'],
)

def dat_etl():


    with TaskGroup("tables_normalizeds") as tg_normalizeds:

        def get_bucket_service():
            return BucketFileService(PostgresWriter(connection="postgres_conn"))

        @task
        def extractor():
            pass   
            return BucketFileLoader('http://storage.googleapis.com/desafio-eng-dados/')\
                .get_files_parquet()


        @task
        def transformer(urls):
            pass
            bucket_file_service = get_bucket_service()
            return bucket_file_service.transformation(urls=urls)

        @task
        def loader(paths):
            pass
            i = 0
            for path in paths:
                if i == 0:
                    bucket_file_service = get_bucket_service()
                    bucket_file_service.loader(path)
                    bucket_file_service.update_process_log()
                i += 1
        @task
        def load_evidence(arg):
            lodimg = ManagerEvidence(PostgresManagerEvidence(connection="postgres_conn"))
            lodimg.manager_evidence(BucketFileLoader('http://storage.googleapis.com/desafio-eng-dados/')\
                            .get_files_img())
            
        dados_transformados = loader(transformer(extractor()))
        load_evidence(dados_transformados)
        


    @task
    def check_status():
        return VerifyProcessLog(PostgresVerifyLog(connection="postgres_conn"))\
            .check_process_log_complete()
    # Checagem após a finalização do primeiro TG
    status_checked = check_status()
    status_checked.set_upstream(tg_normalizeds)


    with TaskGroup("dw") as tg_dw:

        def get_dw_etl():
            return DataWarehouseETL(PostgresWriterDw(connection="postgres_conn"))

        @task
        def extractor():   
            dw = get_dw_etl()
            result = dw.extract()
            print(f'EXECUCAO DO EXTRACTOR {result}')
            return result
            
        
        @task
        def transformer_and_load_dim(data):
            dw = get_dw_etl()
            print(f'DATA RECEBIDA NO TRANSFORMER {data}')
            dw.transform_and_load_dims(data)
            return data
        
        @task
        def load_fct(data):
            dw = get_dw_etl()
            dw.load_fct(data)

        load_fct(transformer_and_load_dim(extractor()))
    
    tg_dw.set_upstream(status_checked)

    with TaskGroup("view") as tg_view:
        @task
        def create_dash():   
            pass
        
        create_dash()    
    tg_view.set_upstream(tg_dw)

# Instantiate the DAG
dat_etl()