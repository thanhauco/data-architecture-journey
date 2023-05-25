from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import logging

# Domain: Marketing

def extract_data(**kwargs):
    logging.info("Extracting data for marketing...")
    # Simulation: Validation logic
    return "s3://landing/marketing/data.csv"

def transform_data(ti, **kwargs):
    s3_path = ti.xcom_pull(task_ids='extract')
    logging.info(f"Transforming data from {s3_path}")
    return "s3://processed/marketing/clean.parquet"

def load_data(ti, **kwargs):
    clean_path = ti.xcom_pull(task_ids='transform')
    logging.info(f"Loading {clean_path} into Warehouse")

default_args = {
    'owner': 'data_eng_marketing',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG('marketing_pipeline_v1', 
         default_args=default_args, 
         schedule_interval='@daily', 
         start_date=datetime(2023, 1, 1),
         catchup=False,
         tags=['marketing', 'production']) as dag:

    start = DummyOperator(task_id='start')
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        provide_context=True
    )
    
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True
    )
    
    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
        provide_context=True
    )
    
    end = DummyOperator(task_id='end')
    
    start >> extract >> transform >> load >> end
