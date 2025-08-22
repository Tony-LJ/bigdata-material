# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
        'complex_dependencies_dag',
        start_date=datetime(2023, 1, 1),
        schedule_interval=timedelta(hours=1),
        catchup=False,
) as dag:

    # 起始任务
    start = EmptyOperator(task_id='start')

    # 第一组并行任务
    task_a1 = BashOperator(
        task_id='task_a1',
        bash_command='echo "Task A1 completed"',
    )

    task_a2 = BashOperator(
        task_id='task_a2',
        bash_command='echo "Task A2 completed"',
    )

    # 中间任务
    middle = BashOperator(
        task_id='middle',
        bash_command='echo "Middle task completed"',
    )

    # 第二组并行任务
    task_b1 = BashOperator(
        task_id='task_b1',
        bash_command='echo "Task B1 completed"',
    )

    task_b2 = BashOperator(
        task_id='task_b2',
        bash_command='echo "Task B2 completed"',
    )

    task_b3 = BashOperator(
        task_id='task_b3',
        bash_command='echo "Task B3 completed"',
    )

    # 结束任务
    end = EmptyOperator(task_id='end')

    # 设置复杂依赖关系
    start >> [task_a1, task_a2] >> middle >> [task_b1, task_b2, task_b3] >> end
