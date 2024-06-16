from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from dotenv import load_dotenv
import json
import os
import boto3

load_dotenv()

def kelvin_to_celsius(temp_in_kelvin):
    temp_in_celsius = (temp_in_kelvin - 273.15)
    return temp_in_celsius

def transform_data(city_name, ti):
    data = ti.xcom_pull(task_ids=f"extract_{city_name}_weather_data_through_api")
    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_celsius = kelvin_to_celsius(data["main"]["temp"])
    feels_like_celsius= kelvin_to_celsius(data["main"]["feels_like"])
    min_temp_celsius = kelvin_to_celsius(data["main"]["temp_min"])
    max_temp_celsius = kelvin_to_celsius(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_celsius,
                        "Feels Like (F)": feels_like_celsius,
                        "Minimun Temp (F)":min_temp_celsius,
                        "Maximum Temp (F)": max_temp_celsius,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)":sunrise_time,
                        "Sunset (Local Time)": sunset_time                        
                        }

    df_new = pd.DataFrame([transformed_data])
    df_data = pd.read_csv(f"weather_data/{city_name}.csv")
    df_data = pd.concat([df_data, df_new])
    df_data.to_csv(f"weather_data/{city_name}.csv", index=False)

def load_data_to_s3_bucket():
    s3 = boto3.resource(
        service_name='s3',
        region_name='ap-southeast-1',
        aws_access_key_id=os.getenv("AWS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET")
    )
    for filename in os.listdir("./weather_data"):
        s3.Bucket('weather-api-airflow-dag-udit').upload_file(Filename=f'./weather_data/{filename}', Key=filename)

default_args = {
    'owner': 'udit',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 16),
    'email': ['email@udit.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


with DAG(
    'weather_dag_etl',
    default_args=default_args,
    schedule_interval = '@daily',
    catchup=False) as dag:

    check_whether_api_ready = HttpSensor(
                                task_id ='check_whether_api_ready',
                                http_conn_id='weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Chennai&APPID={os.getenv('WEATHERMAP_API_KEY')}"
                            )
    
    extract_chennai_weather_data_through_api = SimpleHttpOperator(
                                task_id = 'extract_chennai_weather_data_through_api',
                                http_conn_id = 'weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Chennai&APPID={os.getenv('WEATHERMAP_API_KEY')}",
                                method = 'GET',
                                response_filter= lambda r: json.loads(r.text),
                                log_response=True
                            )
    
    transform_chennai_weather_data = PythonOperator(
                                task_id= 'transform_chennai_weather_data',
                                python_callable=transform_data,
                                op_kwargs={"city_name":"chennai"}
                            )

    
    extract_mumbai_weather_data_through_api = SimpleHttpOperator(
                                task_id = 'extract_mumbai_weather_data_through_api',
                                http_conn_id = 'weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Mumbai&APPID={os.getenv('WEATHERMAP_API_KEY')}",
                                method = 'GET',
                                response_filter= lambda r: json.loads(r.text),
                                log_response=True
                            )
    
    transform_mumbai_weather_data = PythonOperator(
                                task_id= 'transform_mumbai_weather_data',
                                python_callable=transform_data,
                                op_kwargs={"city_name":"mumbai"}
                            )
    

    extract_bengaluru_weather_data_through_api = SimpleHttpOperator(
                                task_id = 'extract_bengaluru_weather_data_through_api',
                                http_conn_id = 'weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Bengaluru&APPID={os.getenv('WEATHERMAP_API_KEY')}",
                                method = 'GET',
                                response_filter= lambda r: json.loads(r.text),
                                log_response=True
                            )
    
    transform_bengaluru_weather_data = PythonOperator(
                                task_id= 'transform_bengaluru_weather_data',
                                python_callable=transform_data,
                                op_kwargs={"city_name":"bengaluru"}
                            )
    

    extract_hyderabad_weather_data_through_api = SimpleHttpOperator(
                                task_id = 'extract_hyderabad_weather_data_through_api',
                                http_conn_id = 'weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Hyderabad&APPID={os.getenv('WEATHERMAP_API_KEY')}",
                                method = 'GET',
                                response_filter= lambda r: json.loads(r.text),
                                log_response=True
                            )
    
    transform_hyderabad_weather_data = PythonOperator(
                                task_id= 'transform_hyderabad_weather_data',
                                python_callable=transform_data,
                                op_kwargs={"city_name":"hyderabad"}
                            )
    

    extract_delhi_weather_data_through_api = SimpleHttpOperator(
                                task_id = 'extract_delhi_weather_data_through_api',
                                http_conn_id = 'weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Delhi&APPID={os.getenv('WEATHERMAP_API_KEY')}",
                                method = 'GET',
                                response_filter= lambda r: json.loads(r.text),
                                log_response=True
                            )
    
    transform_delhi_weather_data = PythonOperator(
                                task_id= 'transform_delhi_weather_data',
                                python_callable=transform_data,
                                op_kwargs={"city_name":"delhi"}
                            )
    
    extract_kolkata_weather_data_through_api = SimpleHttpOperator(
                                task_id = 'extract_kolkata_weather_data_through_api',
                                http_conn_id = 'weathermap_api',
                                endpoint=f"/data/2.5/weather?q=Kolkata&APPID={os.getenv('WEATHERMAP_API_KEY')}",
                                method = 'GET',
                                response_filter= lambda r: json.loads(r.text),
                                log_response=True
                            )
    
    transform_kolkata_weather_data = PythonOperator(
                                task_id= 'transform_kolkata_weather_data',
                                python_callable=transform_data,
                                op_kwargs={"city_name":"kolkata"}
                            )
    

    load_to_s3_bucket = PythonOperator(
                                task_id='load_to_s3_bucket',
                                python_callable=load_data_to_s3_bucket,

                            )

    

    check_whether_api_ready >> extract_chennai_weather_data_through_api >> transform_chennai_weather_data >> load_to_s3_bucket
    check_whether_api_ready >> extract_mumbai_weather_data_through_api >> transform_mumbai_weather_data >> load_to_s3_bucket
    check_whether_api_ready >> extract_bengaluru_weather_data_through_api >> transform_bengaluru_weather_data >> load_to_s3_bucket
    check_whether_api_ready >> extract_hyderabad_weather_data_through_api >> transform_hyderabad_weather_data >> load_to_s3_bucket
    check_whether_api_ready >> extract_delhi_weather_data_through_api >> transform_delhi_weather_data >> load_to_s3_bucket
    check_whether_api_ready >> extract_kolkata_weather_data_through_api >> transform_kolkata_weather_data >> load_to_s3_bucket

    
    