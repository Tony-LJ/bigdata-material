# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
        'parallel_dependencies_dag',
        start_date=datetime(2023, 1, 1),
        schedule_interval=timedelta(hours=1),
        catchup=False,
) as dag:

    # 起始任务
    start_task = BashOperator(
        task_id='start_task',
        bash_command='echo "Starting parallel tasks"',
    )

    # 并行任务
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 10 && echo "Task 1 completed"',
    )

    task_2 = BashOperator(
        task_id='task_2',
        bash_command='sleep 15 && echo "Task 2 completed"',
    )

    task_3 = BashOperator(
        task_id='task_3',
        bash_command='sleep 20 && echo "Task 3 completed"',
    )

    # 结束任务
    end_task = BashOperator(
        task_id='end_task',
        bash_command='echo "All parallel tasks completed"',
    )

    # 设置依赖：start -> [task_1, task_2, task_3] -> end
    start_task >> [task_1, task_2, task_3] >> end_task
