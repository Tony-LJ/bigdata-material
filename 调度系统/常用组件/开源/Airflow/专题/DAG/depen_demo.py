# -*- coding: utf-8 -*-
"""
descr:
author: Tony
date: 2025-08-20
"""
from impala.dbapi import connect
from pymysql import connect as mysql_connect

def config_read_ini():
    host="10.53.0.1"
    port="21050"
    username="root"
    password="szkw.COM202201"
    db_name="bi_ods"
    db_ini = [host,port,username,password,db_name]
    return db_ini

impala_ini = config_read_ini()
mysql_ini = config_read_ini()

# read meta list
def read_meta_lst(meta_sql):
    cursor = connect(impala_ini[0], port=impala_ini[1],user=impala_ini[2],password=impala_ini[3],database=impala_ini[4]).cursor()
    cursor.execute(meta_sql)
    meta_lst = cursor.fetchall()
    print(meta_lst)
    cursor.close()

    return meta_lst


# meta task
meta_sql = f'''select  table_nam 
               from  bi_ods.dask_bi_meta 
               where  run_flag = 1
               and  substring(table_nam,8,4) in ('_dws','ads_')                    
               group by 1  ; '''

bi_meta_lst = read_meta_lst(meta_sql)
bi_meta_lst = [i[0] for i in bi_meta_lst]
print(bi_meta_lst)

depend_sql = f'''select  depend_table ,target_table
                   from  bi_ods.dask_bi_script_depend
                   group by 1,2   ; '''

depend
_sql_lst = read_meta_lst(depend_sql)
depend_sql_lst = [i for i in depend_sql_lst if i[0] in bi_meta_lst]
depend_sql_lst = [i for i in depend_sql_lst if i[1] in bi_meta_lst]
print(depend_sql_lst)

bi_meta_lst = [["bi_ads",i] if "_ads_" in i else ["bi_data",i] for i in bi_meta_lst]
print(bi_meta_lst)

for depend_s in depend_sql_lst:
    dep_name , tar_name = depend_s[0] , depend_s[1]
    print(f"dep_name: {dep_name}, tar_name: {tar_name}")




print(" ---------------------------------------------------------------------------------------------------------------------------------------- ")
def read_mysql_meta_lst(meta_sql):
    cursor = mysql_connect(host="10.53.0.71",port=3306,user="root",password="LJkwhadoop2025!",database="utc").cursor()
    cursor.execute(meta_sql)
    meta_lst = cursor.fetchall()
    print(meta_lst)
    cursor.close()

    return meta_lst

turing_depend_sql = f'''
select n.task_id,
       n.task_file_name,  
       e.dwonstream_task_id
from utc.airflow_dag_task_nodes n
left join utc.airflow_dag_task_edges e on n.task_id = e.upstream_task_id
where n.dag_id='kw_wip_dag'; 
'''
turing_depend_sql_lst = read_mysql_meta_lst(turing_depend_sql)
turing_depend_sql_lst = [i[0] for i in turing_depend_sql_lst]
print(turing_depend_sql_lst)

turing_depend_sqls = read_mysql_meta_lst(turing_depend_sql)
turing_depend_sqls = [i for i in turing_depend_sqls if i[0] in turing_depend_sql_lst]
turing_depend_sqls = [i for i in turing_depend_sqls if i[2] in turing_depend_sql_lst]
print(turing_depend_sqls)


for depend_s in turing_depend_sqls:
    task_id , dwonstream_task_id = depend_s[0] , depend_s[2]
    print(f"task_id: {task_id}, dwonstream_task_id: {dwonstream_task_id}")

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
    cursor = mysql_connect(host="10.53.0.71",port=3306,user="root",password="LJkwhadoop2025!",database="utc").cursor()
    cursor.execute(meta_sql)
    meta_lst = cursor.fetchall()
    cursor.close()

    return meta_lst

dwonstream_task_id = get_dwonstream_task_id('start')
print(" ################################################### ")
print(dwonstream_task_id)