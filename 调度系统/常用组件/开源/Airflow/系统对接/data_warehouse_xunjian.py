# -*- coding: utf-8 -*-
# ################################
# 每天凌晨6点执行一次
# 0 6 * * * /usr/bin/python3 /opt/project/data_warehouse_xunjian.py >> /opt/project/data_warehouse_xunjian.log 2>&1
#
# ###############################

import json
import logging
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
# from impala.dbapi import connect
from datetime import datetime
import pytz
from json import dumps

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"
# AIRFLOW_URL = "http://10.53.1.167:8080/api/v1"
# USERNAME = "luojie"
# PASSWORD = "kw_luojie_241230"
# ##################


class dagBaseInfo:
    """
    dag基础信息实体
    """
    def __init__(self, dag_id, last_excute_start_time, last_excute_end_time, duration):
        self.dag_id = dag_id
        self.last_excute_start_time = last_excute_start_time
        self.last_excute_end_time = last_excute_end_time
        self.duration = duration

    def __str__(self):
        return f"{self.dag_id},{self.last_excute_start_time},{self.last_excute_end_time},{self.duration}"

    def __repr__(self):
        return f'dagBaseInfo(name={self.dag_id}, age={self.last_excute_start_time}, age={self.last_excute_end_time}, age={self.duration})'

    def to_dict(self):
        return {
            'dag_id': self.dag_id,
            'last_excute_start_time': self.last_excute_start_time,
            'last_excute_end_time': self.last_excute_end_time,
            'duration': self.duration
        }

def get_datetime_timezone(iso_str, time_zone, format):
    """
     时区转换计算
    :param iso_str:
    :param time_zone: Asia/Shanghai
    :param format: %Y-%m-%d, %H:%M:%S %Z
    :return:
    """
    # 解析ISO 8601字符串并设置为UTC时区
    utc_dt = datetime.fromisoformat(iso_str).replace(tzinfo=pytz.utc)
    # 定义目标时区（例如CST，即中国标准时间）
    cst_tz = pytz.timezone(time_zone)
    # 将UTC时间转换为CST时间
    cst_dt = utc_dt.astimezone(cst_tz)
    formatted_datetime_str = cst_dt.strftime(format)

    return formatted_datetime_str

def send_wechat_work_message(webhook_url, content, mentioned_list=None):
    """
    发送企业微信机器人消息
    :param webhook_url: 机器人Webhook地址
    :param content: 要发送的文本内容
    :param mentioned_list: 需要@的成员列表(可选)
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content,
            "mentioned_list": mentioned_list
        }
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("消息发送成功")
        return True
    except Exception as e:
        print(f"消息发送失败: {e}")
        return False

if __name__ == '__main__':
    start_timestamp = time.localtime()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_timestamp)
    print(">>>开始进行大数据数仓巡检,巡检日期:{}".format(start_time))
    dag_id_arr = ['kw_ods_dag_new','kw_dwd_dim_dag_new','kw_dws_ads_dag_new']

    dag_base_info_arr = []
    dag_base_info_error_arr = []
    warehouse_total_duration = 0.0

    for dag_id in dag_id_arr:
        url = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        dag_runs = response.json()
        # 获取最新的 DagRun 的开始时间,dag_runs[-1]['dag_run_id']
        latest_dag_run = dag_runs['dag_runs'][-1]
        # latest_dag_run = max(dag_runs['dag_runs'], key=lambda x: x['execution_date'])
        last_dag_start_time = latest_dag_run['start_date'] if 'start_date' in latest_dag_run else latest_dag_run['execution_date']
        last_dag_end_time = latest_dag_run['end_date'] if 'end_date' in latest_dag_run else latest_dag_run['execution_date']
        last_dag_excute_start_time = get_datetime_timezone(last_dag_start_time, 'Asia/Shanghai', '%Y-%m-%d %H:%M:%S')
        last_dag_excute_end_time = get_datetime_timezone(last_dag_end_time, 'Asia/Shanghai', '%Y-%m-%d %H:%M:%S')
        # 计算DAG_ID一次跑完的时间差
        time_difference = datetime.strptime(last_dag_excute_end_time, "%Y-%m-%d %H:%M:%S")  - datetime.strptime(last_dag_excute_start_time, "%Y-%m-%d %H:%M:%S")
        duration = str(time_difference)
        warehouse_total_duration = warehouse_total_duration + time_difference.total_seconds()
        # print(print("时间差:", time_difference))

        dag_base_info = dagBaseInfo(dag_id=dag_id, last_excute_start_time=last_dag_excute_start_time, last_excute_end_time=last_dag_excute_end_time, duration=duration)
        json_str = json.dumps(dag_base_info.to_dict())
        dag_base_info_arr.append(json_str)
        # 根据执行时长判断是否异常,标准不超过3小时
        # print(" time_difference.total_seconds():{}".format(time_difference.total_seconds()))
        if time_difference.total_seconds() > 7200 :
            dag_base_info_error_arr.append(json_str)

    end_timestamp = time.localtime()
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_timestamp)

    msg = ""
    if len(dag_base_info_error_arr) == 0:
        xunjian_result = "正常"
        xunjian_team = "大数据团队"
        utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
        msg = ("<font color='blue'> ** 巡检人员** </font> :  <font color='black'> **" + xunjian_team + "**</font>\n " +
               "<font color='blue'> **巡检日期** </font>: <font color='black'>**" + end_time + "**</font>\n " +
               "<font color='blue'> **整体耗时(h)** </font>: <font color='black'>**" + "{:.2f}".format(warehouse_total_duration/3600) + "**</font>\n " +
               "<font color='blue'> **数仓DAG巡检结果** </font> :  <font color='black'>**" + xunjian_result + "**</font>\n " +
               "<font color='blue'> **数仓DAG详细情况** </font> : \n <font color='black'>" + '\n'.join(dag_base_info_arr) + "</font>\n ")
    else:
        xunjian_result = "异常"
        xunjian_team = "大数据团队"
        utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
        msg = ("<font color='blue'> ** 巡检人员** </font> :  <font color='black'>**" + xunjian_team + "**</font>\n " +
               "<font color='blue'> **巡检日期** </font>: <font color='black'>**" + end_time + "**</font>\n " +
               "<font color='blue'> **整体耗时(h)** </font>: <font color='black'>**" + "{:.2f}".format(warehouse_total_duration/3600) + "**</font>\n " +
               "<font color='blue'> **数仓DAG巡检结果** </font> :  <font color='black'>**" + xunjian_result + "**</font>\n " +
               "<font color='blue'> **数仓DAG详细情况** </font> : \n <font color='black'>" + '\n'.join(dag_base_info_arr) + "</font>\n " +
               "<font color='blue'> **异常DAG列表(执行时间>3小时)** </font> : \n <font color='black'>" + '\n'.join(dag_base_info_error_arr) + "</font>\n ")
    send_wechat_work_message(utcWebhookUrl,msg)
    # print('\n'.join(dag_base_info_arr))
    # print("dag_base_info_arr:{}".format(dag_base_info_arr))



