# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from pymysql import connect

# ########################################################
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

with DAG(
        'customize_complex_dependencies_dag',
        start_date=datetime(2025, 9, 9),
        schedule_interval=timedelta(hours=1),
        catchup=False,
) as dag:
    # 起始任务
    start_task = EmptyOperator(task_id='start_task')

    # 结束任务
    end_task = EmptyOperator(task_id='end_task')

    # # 自定义Sub Dag
    for task_id in dag_task_id_list:
        script_name = task_id
        globals()[script_name] = BashOperator(
            task_id=f'''{script_name}''',
            depends_on_past=False,
            bash_command=f''' echo {script_name} ;" ''',
            dag=dag
        )
        start_task >> globals()[task_id] >> end_task


# 设置复杂依赖关系
for task_id in dag_task_id_list:
    dwonstream_task_id = get_dwonstream_task_id(task_id,dag_task_id_depen_list)
    print(f"task_id: {task_id}, dwonstream_task_id: {dwonstream_task_id}")
    globals()[task_id] >> globals()[dwonstream_task_id]