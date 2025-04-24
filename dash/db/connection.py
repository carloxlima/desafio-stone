import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Você pode definir essas variáveis via .env ou direto aqui
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': os.getenv('DB_PORT', '5432'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'database': os.getenv('DB_NAME', 'dbpedrapagamentos')
}


def get_connection():
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(url)
    return engine


def run_query(sql: str) -> pd.DataFrame:
    engine = get_connection()
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)
