from datetime import datetime
import json
import pandas as pd 
import requests
from  weather_TL import kelvin_to_fahrenheit




city_name = "Passau"
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

with open("dags\weather_api_credentials.txt",'r') as f:
    api_key = f.read()

full_url = base_url + city_name + "&APPID=" + api_key
print(full_url)
r = requests.get(full_url) #response object contain data that is JSON formatted data, we can parse it (analyse it and break it into components)
print(r)

data = r.json()
print(type(data))
print(data)

df_data= pd.DataFrame([data])
df_data.to_csv("D:\\CODE\\airflow\\data.csv")

# city= data["name"]
# weather_description = data["weather"][0]['description']
# temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
# feels_like_farenheit= kelvin_to_fahrenheit(data["main"]["feels_like"])
# min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
# max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
# pressure = data["main"]["pressure"]
# humidity = data["main"]["humidity"]
# wind_speed = data["wind"]["speed"]
# time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
# sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
# sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])


# transformed_data = {"City": city,
#                         "Description": weather_description,
#                         "Temperature (F)": temp_farenheit,
#                         "Feels Like (F)": feels_like_farenheit,
#                         "Minimun Temp (F)":min_temp_farenheit,
#                         "Maximum Temp (F)": max_temp_farenheit,
#                         "Pressure": pressure,
#                         "Humidty": humidity,
#                         "Wind Speed": wind_speed,
#                         "Time of Record": time_of_record,
#                         "Sunrise (Local Time)":sunrise_time,
#                         "Sunset (Local Time)": sunset_time                        
#                         }

# transformed_data_list = [transformed_data]
# df_data = pd.DataFrame(transformed_data_list) #https://www.geeksforgeeks.org/python-pandas-dataframe/   
#                                         # Pandas DataFrame is two-dimensional size-mutable, data is aligned in a tabular fashion in rows and columns
#                                         # Dataframe can be created from a list(1 colums named 0 with values = list items) or dictionary
#                                         # data = {'Name':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]} 
#                                         # where Name and Age are the keys and columns names and value is data in respective columns
# print("type = ",type(df_data),df_data)
