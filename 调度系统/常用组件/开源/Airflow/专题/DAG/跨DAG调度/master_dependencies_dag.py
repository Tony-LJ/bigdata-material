# -*- coding: utf-8 -*-
"""
descr : Airflow Dag Task自定血缘关系开发关系脚手架
auther : lj.michale
create_date : 2025/2/19 15:54
file_name : master_dependencies_dag.py
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
        dag_id="master_dag",
        default_args=default_args,
        schedule_interval="13,23,33,43,53 12,13,14,15,16,17 * * *",
        #concurrency=1,
        #max_active_runs=1,
        tags=['example1'],
) as child_dag:
    # [START howto_operator_external_task_sensor]
    child_task1 = ExternalTaskSensor(
        task_id="master_task1",
        external_dag_id="slave_dag",
        external_task_id="slave_task1",
        timeout=120,
        allowed_states=['success'],
        failed_states=['failed', 'skipped'],
        execution_delta=timedelta(minutes=3),
        mode= "reschedule",
    )

    # [END howto_operator_external_task_sensor]
    child_task2 = BashOperator(task_id="master_task2",bash_command="echo i am master!",dag=child_dag)
child_task1 >> child_task2


