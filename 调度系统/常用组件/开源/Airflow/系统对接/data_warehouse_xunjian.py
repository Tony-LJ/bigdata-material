# -*- coding: utf-8 -*-
# ################################
# */10 * * * * /usr/bin/python3 /opt/project/data_warehouse_xunjian.py >> /opt/project/data_warehouse_xunjian.log 2>&1
#
# ###############################

import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
# from impala.dbapi import connect
from datetime import datetime
import pytz

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"
# ##################


def get_datetime_timezone(iso_str, time_zone, format):
    """
     时区转换计算
    :param iso_str:
    :param time_zone: Asia/Shanghai
    :param format: %Y-%m-%d, %H:%M:%S %Z
    :return:
    """
    # 解析ISO 8601字符串并设置为UTC时区
    utc_dt = datetime.fromisoformat(iso_str)
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    # 定义目标时区（例如CST，即中国标准时间）
    cst_tz = pytz.timezone(time_zone)
    # 将UTC时间转换为CST时间
    cst_dt = utc_dt.astimezone(cst_tz)
    formatted_datetime_str = cst_dt.strftime(format)

    return formatted_datetime_str

if __name__ == '__main__':
    start_timestamp = time.localtime()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_timestamp)
    print(">>>开始进行大数据数仓巡检,巡检日期:{}".format(start_time))
    dag_id = 'kw_dwd_dim_dag_new'
    url = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    dag_runs = response.json()
    print(dag_runs)
    # 获取最新的 DagRun 的开始时间
    latest_dag_run = max(dag_runs['dag_runs'], key=lambda x: x['execution_date'])
    print(latest_dag_run)
    dag_start_time = latest_dag_run['start_date'] if 'start_date' in latest_dag_run else latest_dag_run['execution_date']
    # 解析ISO 8601字符串并设置为UTC时区
    iso_str = dag_start_time
    utc_dt = datetime.fromisoformat(iso_str)
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    # 定义目标时区（例如CST，即中国标准时间）
    cst_tz = pytz.timezone('Asia/Shanghai')
    # 将UTC时间转换为CST时间
    cst_dt = utc_dt.astimezone(cst_tz)
    formatted_str = cst_dt.strftime('%Y-%m-%d, %H:%M:%S %Z')

    print("Latest DagRun Start Time:", formatted_str)
    print(get_datetime_timezone(dag_start_time, 'Asia/Shanghai', '%Y-%m-%d, %H:%M:%S %Z'))


    end_timestamp = time.localtime()
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_timestamp)
    print(">>>开始进行大数据数仓巡检,巡检日期:{}".format(end_time))

