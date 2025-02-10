from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess

#Initialize database and create tables
def run_initialize_db():
    subprocess.run(["python", "/opt/airflow/app/initialize_db.py"])

#Extract and clean the data
def run_extract_transform_load():
    subprocess.run(["python", "/opt/airflow/app/extract_transform_load.py"])

#Load the cleaned data to csv
def run_load_csv_to_db():
    subprocess.run(["python", "/opt/airflow/app/load_csv_to_db.py"])

default_args = {
    'owner': 'Praveen Manikyam',
    'retries': 1,
    'start_date': datetime(2025, 2, 5),
}

dag = DAG(
    'fpl_api_flow',
    default_args=default_args,
    description='ETL workflow to initialize DB, fpl scripts and load CSV data',
    schedule_interval=None,
)

task1 = PythonOperator(
    task_id='initialize_db',
    python_callable=run_initialize_db,
    dag=dag,
)

task2 = PythonOperator(
    task_id='extract_transform_load',
    python_callable=run_extract_transform_load,
    dag=dag,
)

task3 = PythonOperator(
    task_id='load_csv_to_db',
    python_callable=run_load_csv_to_db,
    dag=dag,
)

task1 >> task2 >> task3
