# -*- coding: utf-8 -*-
"""
descr : Airflow Dag Task自定血缘关系开发关系脚手架
auther : lj.michale
create_date : 2025/2/19 15:54
file_name : slave_dependencies_dag.py
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.sensors.external_task_sensor import ExternalTaskMarker, ExternalTaskSensor
import pendulum

local_tz = pendulum.timezone("Asia/Shanghai")
default_args={
    "owner": "airflow",
    "start_date": datetime(2022, 9, 20, 11, 0,tzinfo=local_tz),
}
with DAG(
        dag_id="slave_dag",
        default_args=default_args,
        schedule_interval="10,20,30,40,50 12,13,14,15,16,17 * * *",
        #concurrency=1,
        #max_active_runs=1,
        tags=['example2'],
) as slave_dag:
    # [START howto_operator_external_task_marker]
    '''
    parent_task = ExternalTaskMarker(
     task_id="slave_task2",
     external_dag_id="master_dag",
     external_task_id="master_task1",
     execution_delta=timedelta(minutes=3)
      )
parent_task
'''
    slave_task = BashOperator(
        task_id ="slave_task1",
        bash_command ="echo i am slave!",
    )

slave_task

