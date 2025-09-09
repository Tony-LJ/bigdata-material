# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from pymysql import connect

def read_mysql_meta_lst(meta_sql):
    cursor = connect(host="10.53.0.71",port=3306,user="root",password="LJkwhadoop2025!",database="utc").cursor()
    cursor.execute(meta_sql)
    meta_lst = cursor.fetchall()
    print(meta_lst)
    cursor.close()

    return meta_lst

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
    dwonstream_task_id = cursor.fetchall()
    cursor.close()

    return dwonstream_task_id


def get_task_list():
    """
    获取下游task_id
    :param task_id:
    :return:
    """
    cursor = connect(host="10.53.0.71",port=3306,user="root",password="LJkwhadoop2025!",database="utc").cursor()
    sql = """
        select n.task_id
        from utc.airflow_dag_task_nodes n
        where n.dag_id='kw_wip_dag'
    """
    cursor.execute(sql)
    task_id_list = cursor.fetchall()
    cursor.close()

    return task_id_list

task_id_list = get_task_list()

turing_depend_sql = f'''
select n.task_id,
       n.task_file_name,  
       e.dwonstream_task_id
from utc.airflow_dag_task_nodes n
left join utc.airflow_dag_task_edges e on n.task_id = e.upstream_task_id
where n.dag_id='kw_wip_dag'
'''

turing_depend_sql_lst = read_mysql_meta_lst(turing_depend_sql)
turing_depend_sql_lst = [i[0] for i in turing_depend_sql_lst]
print(turing_depend_sql_lst)

turing_depend_sqls = read_mysql_meta_lst(turing_depend_sql)
turing_depend_sqls = [i for i in turing_depend_sqls if i[0] in turing_depend_sql_lst]
turing_depend_sqls = [i for i in turing_depend_sqls if i[2] in turing_depend_sql_lst]
print(turing_depend_sqls)

# ########################################################
my_list = ['start',
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

with DAG(
        'customize_complex_dependencies_dag',
        start_date=datetime(2025, 9, 6),
        schedule_interval=timedelta(hours=1),
        catchup=False,
) as dag:
    # 起始任务
    start_task = EmptyOperator(task_id='start_task')

    # 结束任务
    end_task = EmptyOperator(task_id='end_task')

    # # 自定义Sub Dag
    for task_id in my_list:
        script_name = task_id
        globals()[script_name] = BashOperator(
            task_id=f'''{script_name}''',
            depends_on_past=False,
            bash_command=f''' echo {script_name} ;" ''',
            dag=dag
        )
        start_task >> globals()[task_id] >> end_task


# 设置复杂依赖关系
for task_id in task_id_list:
    dwonstream_task_id = get_dwonstream_task_id(task_id)
    print(f"task_id: {task_id}, dwonstream_task_id: {dwonstream_task_id}")
    globals()[task_id] >> globals()[dwonstream_task_id]