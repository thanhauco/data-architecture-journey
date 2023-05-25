from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import logging

# Domain: Product

def extract_data(**kwargs):
    logging.info("Extracting data for product...")
    # Simulation: Validation logic
    return "s3://landing/product/data.csv"

def transform_data(ti, **kwargs):
    s3_path = ti.xcom_pull(task_ids='extract')
    logging.info(f"Transforming data from {s3_path}")
    return "s3://processed/product/clean.parquet"

def load_data(ti, **kwargs):
    clean_path = ti.xcom_pull(task_ids='transform')
    logging.info(f"Loading {clean_path} into Warehouse")

default_args = {
    'owner': 'data_eng_product',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG('product_pipeline_v1', 
         default_args=default_args, 
         schedule_interval='@daily', 
         start_date=datetime(2023, 1, 1),
         catchup=False,
         tags=['product', 'production']) as dag:

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
