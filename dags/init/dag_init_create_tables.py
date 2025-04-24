from airflow.decorators import dag, task
from pendulum import datetime
from src.repositories.postgres_create_tables import PostgresCreateTables


@dag(
    dag_id="init_create_tables",
    schedule_interval="@once",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"owner": "Carlos", "retries": 0},
    tags=["init", "start_on_boot"],
)
@task
def create_tables():
    creat_tb = PostgresCreateTables(connection="postgres_conn")
    creat_tb.create_tables_models()
    print("Tables created successfully.")


# Instantiate the DAG
create_tables()
