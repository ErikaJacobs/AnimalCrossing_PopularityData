# Airflow DAG

from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Default Argument

default_args = {
    'owner': 'airflow',    
    'start_date': airflow.utils.dates.days_ago(1),
    # 'end_date': datetime(2018, 12, 30),
    'depends_on_past': True,
    'email': ['ErikaAshley3@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'provide_context': True}

# DAG

dag = DAG(
    'ACNH_Popularity',
    default_args=default_args,
    description='Scrapes Animal Crossing Villager data and sends to MySQL',
    schedule_interval='0 0 1,15 * *')

# Tasks

# Set Working Directory

# Input - Script Directory
file =  '/mnt/c/Users/cluel/Documents/GitHub/Animal-Crossing-Popularity-Data'

####################################

# Import Class
from scripts import acnh_pop as ac
cl = ac.acnh_pop_class()

# Create Tasks
t1 = PythonOperator(task_id='scrape_web_data', python_callable = cl.acnGetPopData, dag=dag)
t2 = PythonOperator(task_id='df_and_mysql', python_callable = cl.getVillagerInfo, dag=dag)

# Task Organization

t1 >> t2