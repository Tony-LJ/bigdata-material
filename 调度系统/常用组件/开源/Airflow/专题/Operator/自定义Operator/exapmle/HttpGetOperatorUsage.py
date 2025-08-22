# -*- coding: utf-8 -*-
"""
descr: 如何使用HttpGetOperator
author: tony
date: 2025-08-20
"""
from airflow import DAG
from datetime import datetime, timedelta
from custom_http_operator import HttpGetOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_custom_http_dag',
    default_args=default_args,
    description='A simple DAG that uses a custom HTTP GET operator',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# 使用自定义的HttpGetOperator
http_task = HttpGetOperator(
    task_id='http_get_task',
    endpoint='https://api.example.com/data',
    params={'key': 'value'},
    dag=dag,
)
