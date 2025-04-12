from airflow.decorators import dag, task
from pendulum import datetime
from src.repositories.postgres_create_database import PostgresCreateDatabase


@dag(
    dag_id="init_create_dbpedrapagamentos",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"owner": "Carlos", "retries": 0},
    tags=["init","new_database","leticinha"],
)


def create_dbpedrapagamentos():

    @task
    def create_db():   
        PostgresCreateDatabase(connection="postgres_conn").create_database(database_name="dbpedrapagamentos")
    
    create_db()
        
# Instantiate the DAG
create_dbpedrapagamentos()