from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor # sensor operator that waits for a certain condition related to an HTTP endpoint to be met before allowing the DAG to proceed
import json
from airflow.providers.http.operators.http import SimpleHttpOperator # operator used for making HTTP requests(GET,POST,PUT) as part of a workflow
from airflow.operators.python import PythonOperator
import pandas as pd #working with data sets: include functions for analyzing, cleaning, exploring, and manipulating data
import requests
import os
import boto3

# Set up AWS credentials
aws_access_key_id = 'AKIAZQ3DT37DE7E7UTFW'
aws_secret_access_key = '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'

#Create an S3 client:
s3 = boto3.client('s3', 
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# bucket_name = 'weatherapiproject'
# key = 'weather_data/'  # The path in S3 where you want to save the file





############################### using PythonOperator #####################################

def extract_data():
    city_name = "Passau"
    base_url = "https://api.openweathermap.org/data/2.5/weather?q="

    # with open("dags\weather_api_credentials.txt",'r') as f:
    #     api_key = f.read()

    full_url = base_url + city_name + "&APPID=" + "9555a6fbad86a57efd0233c83b678fc3"

    # Send a GET request to the API
    r = requests.get(full_url)

    # Parse the JSON data from the response
    data = r.json()
    print(data)

    return data

data = extract_data()
print(type(data))
print(data) 

# data = extract_data()
# print(data)

# def show(ti):
#     data = ti.xcom_pull(task_id = 'extract_weather_data',key = data)
#     df_data = pd.DataFrame(data)
#     print("YEEEEEEEEEEEEEEEEEEEEEEEEEES")
#     return 1



##################################### Transfor & load ###############################################

def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit


def transform_load_data(ti):
    print("hello")
    data=ti.xcom_pull(task_ids = 'extract_weather_data')
    # print(data)
    city= data["name"]
    weather_description = data["weather"][0]['description']
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit= kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])


    transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_farenheit,
                        "Feels Like (F)": feels_like_farenheit,
                        "Minimun Temp (F)":min_temp_farenheit,
                        "Maximum Temp (F)": max_temp_farenheit,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)":sunrise_time,
                        "Sunset (Local Time)": sunset_time                        
                        }

    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)
    print(df_data)

    aws_credentials = {"key": "xxxxxxxxx", "secret": "xxxxxxxxxx", "token": "xxxxxxxxxxxxxx"}


    # print("hello")
    # df_data.to_csv("D:\\CODE\\airflow\\data.csv")
    

    # now = datetime.now() # now's time
    # dt_string = now.strftime("%d%m%Y%H%M%S") #convert time into a string day-month-year-hours-seconds
    # dt_string = 'current_weather_data_Passau_' + dt_string #name of the CSV file
    # df_data.to_csv(f"{dt_string}.csv",index=False)

    directory_path = "D:\\CODE\\airflow"

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    os.chmod(directory_path, 0o777)

    now = datetime.now().strftime("%d%m%Y%H%M%S")
    file_path = os.path.join(directory_path, f"current_weather_data_Passau_{now}.csv")
    df_data.to_csv(file_path, index=False)

    # df_data.to_csv(f"s3://weatherapiairflowyoutubebucket-yml/{dt_string}.csv", index=False) #creation of a CSV file for a specific time (DAG execution)

