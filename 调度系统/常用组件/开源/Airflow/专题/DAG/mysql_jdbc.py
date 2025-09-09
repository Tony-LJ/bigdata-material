# -*- coding: utf-8 -*-
"""
descr:
author: Tony
date: 2025-08-20
"""
from itertools import groupby

from pymysql import connect

def get_dwonstream_task_id(task_id):
    """
    获取下游task_id
    :param task_id:
    :return:
    """
    meta_sql = f'''
        select n.task_id,
               n.task_file_name,  
               e.dwonstream_task_id
        from utc.airflow_dag_task_nodes n
        left join utc.airflow_dag_task_edges e on n.task_id = e.upstream_task_id
        where n.dag_id='kw_wip_dag'
        and n.task_id = '{task_id}'
    '''
    cursor = connect(host="10.53.0.71",port=3306,user="root",password="LJkwhadoop2025!",database="utc").cursor()
    cursor.execute(meta_sql)
    meta_lst = cursor.fetchall()
    cursor.close()

    return meta_lst


dwonstream_task_id = get_dwonstream_task_id('start')
print(" ###################################################################################################### ")
print(dwonstream_task_id)


print(" ###################################################################################################### ")
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

print(dag_task_id_list)
print(dag_task_id_depen_list)

print(" ###################################################################################################### ")
# tuples = [('a', 'a1'), ('a', 'a2'), ('b', 'b1'), ('b', 'b2'), ('c', 'c1'), ('c', 'c2')]
tuples = [('start','ODS_APPS_WIP_DISCRETE_JOBS_V'),
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

result = {k: [] for k in {t[0] for t in tuples}}

for t in tuples:
    result[t[0]].append(t[1])

print(result["ODS_APPS_WIP_DISCRETE_JOBS_V"])
print(get_dwonstream_task_id('bi_data_dws_wip_online_bala_ds', dag_task_id_depen_list))





















