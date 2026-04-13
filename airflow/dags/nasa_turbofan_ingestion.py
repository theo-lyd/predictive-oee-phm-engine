from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 4, 12),
    'retries': 1,
}

dag = DAG(
    'nasa_turbofan_ingestion',
    default_args=default_args,
    description='Ingest NASA Turbofan Failure Data via Kaggle CLI',
    schedule_interval=None,
    catchup=False,
)

download_nasa_turbofan = BashOperator(
    task_id='download_nasa_turbofan',
    bash_command='bash /workspace/scripts/download_nasa_turbofan.sh',
    dag=dag,
)
