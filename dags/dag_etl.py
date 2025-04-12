from airflow import DAG
from airflow.operators.python import PythonOperator     
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

import polars as pl
import os

dag = DAG(
    'dag_etl',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2025, 12, 4),
        'retries': 1,
    },
    schedule_interval='@daily',
    catchup=False,
    tags=['extractor', 'transformer', 'loader']
)


