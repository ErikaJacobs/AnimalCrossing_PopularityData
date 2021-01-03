# Airflow DAG

from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
#import ac_pop as ac
from AnimalCrossing_PopularityData import ac_pop as ac

# Default Argument

default_args = {
    'owner': 'airflow',    
    'start_date': airflow.utils.dates.days_ago(1),
    # 'end_date': datetime(2021, 12, 30),
    'depends_on_past': True,
    'email': ['ErikaAshley3@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'provide_context': True}

# DAG
dag = DAG(
    'AC_Pop',
    default_args=default_args,
    description='Scrapes Animal Crossing Villager data and sends to MySQL',
    schedule_interval='0 0 1,15 * *')

####################################

# Set Class
acnh = ac.AC_Pop()

# Create Tasks
t1 = PythonOperator(task_id='create_df', python_callable = acnh.create_df, dag=dag)
t2 = PythonOperator(task_id='kaggle_data', python_callable = acnh.kaggle_data, dag=dag)
t3 = PythonOperator(task_id='join_tables', python_callable = acnh.join_tables, dag=dag)
t4 = PythonOperator(task_id='send_mysql', python_callable = acnh.send_mysql, dag=dag)
t5 = PythonOperator(task_id='cleanup', python_callable = acnh.cleanup, dag=dag)

# Task Organization

t1 >> t2
t2 >> t3
t3 >> t4
t4 >> t5