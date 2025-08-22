# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
        'linear_dependencies_dag',
        start_date=datetime(2023, 1, 1),
        schedule_interval=timedelta(hours=1),
        catchup=False,
) as dag:

    # 创建多个任务
    task_a = BashOperator(
        task_id='task_a',
        bash_command='echo "Task A completed"',
    )

    task_b = BashOperator(
        task_id='task_b',
        bash_command='echo "Task B completed"',
    )

    task_c = BashOperator(
        task_id='task_c',
        bash_command='echo "Task C completed"',
    )

    task_d = BashOperator(
        task_id='task_d',
        bash_command='echo "Task D completed"',
    )

    # 设置线性依赖：A -> B -> C -> D
    task_a >> task_b >> task_c >> task_d
