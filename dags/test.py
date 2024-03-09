from airflow import DAG
from airflow import settings
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor # sensor operator that waits for a certain condition related to an HTTP endpoint to be met before allowing the DAG to proceed
import json
import os 
import requests
from airflow.providers.http.operators.http import SimpleHttpOperator # operator used for making HTTP requests(GET,POST,PUT) as part of a workflow
from airflow.operators.python import PythonOperator
import pandas as pd #working with data sets: include functions for analyzing, cleaning, exploring, and manipulating data


def f1():
    data = {'Name':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]}
    return data

def f2(ti):
    data =ti.xcom_pull(task_id = 'generate_data')
    print(data)
    return 1



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 6),
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}


with DAG('hello_dag', default_args=default_args, schedule_interval = None, catchup=False) as dag:

    t1= PythonOperator(
        task_id = 'generate_data',
        python_callable=f1
    )

    t2 = PythonOperator(
        task_id = 'compute_data',
        python_callable=f2
    )


    t1 >> t2 