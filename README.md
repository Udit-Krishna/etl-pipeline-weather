# Automated ETL pipeline for weather data of 6 Indian cities

This repository contains an automated ETL (Extract, Transform, Load) pipeline for weather data of six Indian cities: Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, and Kolkata. The ETL pipeline is controlled by Apache Airflow and utilizes the OpenWeatherMap API to extract weather data. The extracted data is transformed into a Pandas DataFrame and then loaded onto an S3 bucket for storage.

## Architecture
**Extraction**: Weather data is extracted from the OpenWeatherMap API for Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, and Kolkata.
**Transformation**: The extracted data is transformed into a Pandas DataFrame, ensuring a consistent and structured format.
**Loading**: The transformed data is loaded into an S3 bucket for storage.
The pipeline is orchestrated using Apache Airflow, ensuring reliable and scalable execution.