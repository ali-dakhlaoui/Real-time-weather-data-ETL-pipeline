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
from weather_TL import  transform_load_data
from weather_TL import extract_data





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

with DAG('weather_dag', default_args=default_args, schedule_interval = None, catchup=False) as dag:


    is_weather_api_ready = HttpSensor(
        task_id = 'is_weather_api_ready',
        http_conn_id = 'weathermap_api',
        endpoint='/data/2.5/weather?q=Passau&appid=9555a6fbad86a57efd0233c83b678fc3'
    )
    
    extract_weather_data = PythonOperator(
        task_id = 'extract_weather_data',
        python_callable=extract_data
    )



    # extract_weather_data = SimpleHttpOperator (
    #     task_id = 'extract_weather_data',
    #     http_conn_id = 'weathermap_api',
    #     endpoint='/data/2.5/weather?q=Passau&appid=9555a6fbad86a57efd0233c83b678fc3',
    #     headers = {
    #             'q' : 'Passau',
    #             'appid' : '9555a6fbad86a57efd0233c83b678fc3'
    #     },
    #     method= 'GET',
    #     response_filter = lambda response: response.json(), 
    #     # lambda function (anonym) with format func = lambda r(response object as variable): 
    #     # exression of a function (here is json.load(r.text))
    #     #r.text extract information from the response, transform that HTTP respone (JSON-format string) into Python dictionnary
    #     log_response = True # details of the HTTP response, such as the status code, headers, and response body, will be recorded in the Airflow task logs.
    #     ,dag = dag
    # )




    transform_load_weather_data = PythonOperator(
        task_id =  'transform_load_weather_data',
        python_callable= transform_load_data 
    )

    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data

