# -*- coding: utf-8 -*-
"""
descr : kw_spark_ods_dag数据同步DAG
auther : lj.michale
create_date : 2025/2/19 15:54
file_name : kw_spark_ods_dag.py
"""
import pendulum
import airflow
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import pandas as pd
from datetime import timedelta
from datetime import datetime
from impala.dbapi import connect
import configparser
import logging
import requests
import time

# ################## 公共参数 #######################################
ini_path =  "/root/airflow/dags/profile_kw.ini"
context='999999'
dag_name = 'customize_complex_dependencies_dag'
# ##################################################################

# DAG Task 任务列表
dag_task_id_list = ['start',
                    'ODS_CUX_MES_ONLINE_BALA_T',
                    'ODS_APPS_WIP_DISCRETE_JOBS_V',
                    'fine_bi_dws_wip_online_bala_ds',
                    'fine_bi_ads_wip_online_bala_info_ds',
                    'fine_bi_ads_wip_online_bala_detail_ds',
                    'bi_data_dws_wip_online_bala_ds',
                    'bi_data_dwd_cux_mes_online_bala',
                    'bi_data_dwd_apps_wip_discrete_jobs_v',
                    'bi_ads_ads_wip_online_bala_info_ds',
                    'bi_ads_ads_wip_online_bala_detail_ds',
                    'end'
                    ]

# DAG Task 任务依赖关系列表
dag_task_id_depen_list = [('start','ODS_APPS_WIP_DISCRETE_JOBS_V'),
                          ('start','ODS_CUX_MES_ONLINE_BALA_T'),
                          ('ODS_APPS_WIP_DISCRETE_JOBS_V','bi_data_dwd_apps_wip_discrete_jobs_v'),
                          ('ODS_CUX_MES_ONLINE_BALA_T','bi_data_dwd_cux_mes_online_bala'),
                          ('fine_bi_dws_wip_online_bala_ds','end'),
                          ('fine_bi_ads_wip_online_bala_info_ds','end'),
                          ('fine_bi_ads_wip_online_bala_detail_ds','end'),
                          ('end',''),
                          ('bi_data_dws_wip_online_bala_ds','fine_bi_dws_wip_online_bala_ds'),
                          ('bi_data_dws_wip_online_bala_ds','bi_ads_ads_wip_online_bala_info_ds'),
                          ('bi_data_dws_wip_online_bala_ds','bi_ads_ads_wip_online_bala_detail_ds'),
                          ('bi_data_dwd_cux_mes_online_bala','bi_data_dws_wip_online_bala_ds'),
                          ('bi_data_dwd_apps_wip_discrete_jobs_v','bi_data_dws_wip_online_bala_ds'),
                          ('bi_ads_ads_wip_online_bala_info_ds','fine_bi_ads_wip_online_bala_detail_ds'),
                          ('bi_ads_ads_wip_online_bala_detail_ds','fine_bi_ads_wip_online_bala_info_ds')
                          ]

def get_dwonstream_task_id(task_id, tuples):
    """
    查询dwonstream_task_id
    :param task_id
    :param tuples
    :return
    """
    result = {k: [] for k in {t[0] for t in tuples}}
    for t in tuples:
        result[t[0]].append(t[1])

    return result[task_id]

# 默认参数
default_args = {
    'owner': 'luojie',
    'depends_on_past': False,
    'start_date': pendulum.yesterday(tz="Asia/Shanghai"),
    'email': ['jie.luo2@kinwong.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=8),
    'concurrency': 12
}

dag = DAG(
    dag_id=f'''{dag_name}''',
    default_args=default_args,
    description=f'''{dag_name}''',
    schedule='32 2 * * *'
)

start_task = EmptyOperator(task_id='start_task')

end_task = EmptyOperator(task_id='end_task')

# 自定义Sub Dag
for task_id in dag_task_id_list:
    script_name = task_id
    globals()[script_name] = BashOperator(
        task_id=f'''{script_name}''',
        depends_on_past=False,
        bash_command=f''' ssh root@10.53.0.71 "echo {script_name} ;" ''',
        dag=dag
    )
    # start_task >> globals()[task_id] >> end_task

# 设置复杂依赖关系
for task_id in dag_task_id_list:
    if task_id != 'end':
        dwonstream_task_id_list = get_dwonstream_task_id(task_id,dag_task_id_depen_list)
        for dwonstream_task_id in dwonstream_task_id_list:
            print(f"task_id: {task_id}, dwonstream_task_id: {dwonstream_task_id}")
            globals()[task_id] >> globals()[dwonstream_task_id]
    elif task_id == 'end':
        print("不用管")

