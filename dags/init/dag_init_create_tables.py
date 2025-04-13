from airflow.decorators import dag, task
from pendulum import datetime
from src.repositories.postgres_create_tables import PostgresCreateTables



@dag(
    dag_id="init_create_tables",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"owner": "Carlos", "retries": 0},
    tags=["init","new_database"]
)

@task
def create_tables():

        PostgresCreateTables(connection="postgres_conn").create_tables()
    
        
# Instantiate the DAG
create_tables()