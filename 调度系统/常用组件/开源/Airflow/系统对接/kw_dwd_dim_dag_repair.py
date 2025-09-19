# -*- coding: utf-8 -*-
# ################################
# descr: airflow新集群kw_dwd_dim_dag异常情况巡检修复脚本
# author: Tony
# date: 2025-09-18
# */20 * * * * sshpass -p 'EEEeee111' ssh root@10.53.0.75 python3 /srv/tmp/kw_dwd_dim_dag_repair.py >> /opt/project/kw_dwd_dim_dag_repair.log 2>&1
# ###############################

import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
# from impala.dbapi import connect

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"
# ##################

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

def get_csrf_token():
    session = requests.Session()
    # 第一步：获取 CSRF token
    login_page = session.get(f'http://10.53.0.75:8080/login')
    soup = BeautifulSoup(login_page.text, 'html.parser')

    # 提取 CSRF token
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    return csrf_token, session

def get_airflow_health():
    """
    获取Airflow健康状态
    :return:
    """
    url = f"{AIRFLOW_URL}/health"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def retry_failed_taskId_InDag(dag_id):
    """
    DAG失败Task实例重启
    :param dag_id:
    :return:
    """
    AIRFLOW_URL = "http://10.53.0.75:8080"
    USERNAME = "airflow"
    PASSWORD = "airflow"
    session = requests.Session()
    login_page = session.get(f'{AIRFLOW_URL}/login')
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    print("csrf_token:{}".format(csrf_token))
    credentials = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrf_token': csrf_token  # 添加 CSRF token
    }
    response = session.post(f'{AIRFLOW_URL}/login', data=credentials)
    api_url = f'{AIRFLOW_URL}/api/v1/dags'
    response = session.get(api_url)
    # 获取指定dag的信息
    api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns'
    response = session.get(api_url)
    # 获取最新dagRuns
    dag_runs = response.json()['dag_runs']
    last_dag_run_id = dag_runs[-1]['dag_run_id']
    # 获取任务状态
    api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns/{last_dag_run_id}/taskInstances'
    # print(api_url)
    taskInstances = session.get(api_url).json()['task_instances']
    up_for_retry_tasks =[]
    failed_tasks =[]
    for taskInstance in taskInstances:
        task_id = taskInstance['task_id']
        state = taskInstance['state']
        # worker任务执行失败/超时
        if state == 'failed':
            failed_tasks.append(task_id)
            pass
        # task已failed但尚未进入retry状态
        if state == 'up_for_retry':
            up_for_retry_tasks.append(task_id)
            pass
        pass
    execution_date = last_dag_run_id.split('__')[1]

    # 异常任务&正常任务判断与处理逻辑
    if len(failed_tasks) > 0:
        print("worker任务执行失败/超时")
        for task_id in failed_tasks:
            data = {
                'csrf_token': csrf_token,
                'dag_id': dag_id,
                'dag_run_id': last_dag_run_id,
                'task_id': task_id,
                'confirmed': 'true',
                "downstream": 'true',
                "recursive": 'true',
                'execution_date': execution_date
            }
            try:
                response = session.post(f'{AIRFLOW_URL}/clear',data=data, verify=False)
                print(response.text)
            except:
                utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
                msg = "**DAG名称**: <font color='blue'>" + dag_id + "</font>\n " + "**Task名称**: <font color='blue'>" + task_id + "</font>\n" + "**执行日期**: <font color='blue'>" + execution_date + "</font>\n" + "**异常原因**: <font color='blue'>" + response.text + "</font>\n"
                send_wechat_work_message(utcWebhookUrl,msg)
                print("发现Task=fail状态任务，并重新拉起失败，请立即检查!", response.status_code, response.text)
    elif len(up_for_retry_tasks) > 0:
        print("task已failed但尚未进入retry状态")
        for task_id in up_for_retry_tasks:
            data = {
                'csrf_token': csrf_token,
                'dag_id': dag_id,
                'dag_run_id': last_dag_run_id,
                'task_id': task_id,
                'confirmed': 'true',
                "downstream": 'true',
                "recursive": 'true',
                'execution_date': execution_date
            }
            try:
                response = session.post(f'{AIRFLOW_URL}/clear',data=data, verify=False)
                print(response.text)
            except:
                utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
                msg = "**DAG名称**: <font color='blue'>" + dag_id + "</font>\n " + "**Task名称**: <font color='blue'>" + task_id + "</font>\n" + "**执行日期**: <font color='blue'>" + execution_date + "</font>\n" + "**异常原因**: <font color='blue'>" + response.text + "</font>\n"
                send_wechat_work_message(utcWebhookUrl,msg)
                print("发现Task=up_for_retry状态任务，并重新拉起失败，请注意检查!", response.status_code, response.text)
    else:
        print("巡检过程未发现异常Task时的处理逻辑")
        struct_time = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        print(">>>>>无异常任务,巡检时间:{}".format(current_time))
        # utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
        # msg = "**DAG巡检结果**: <font color='blue'> " + dag_id + "无异常任务,巡检日期:" + current_time + " </font>\n "
        # send_wechat_work_message(utcWebhookUrl,msg)


if __name__ == '__main__':
    start_time = time.time()
    print("DAG:kw_dwd_dim_dag异常情况巡检开始!")
    csrf_token, session = get_csrf_token()
    print("airflow_csrf_token:{}, airflow_session:{}".format(csrf_token, session))
    print(" >>>>>> Airflow健康度检查" )
    health = get_airflow_health()
    if health:
        print(f"Metadatabase status: {health['metadatabase']['status']}")
        print(f"Scheduler status: {health['scheduler']['status']}")
    # 巡检DAG:kw_dwd_dim_dag_new
    xunjian_dags = 'kw_dwd_dim_dag_new'
    retry_failed_taskId_InDag(xunjian_dags)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"DAG:kw_dwd_dim_dag异常情况巡检开始结束: {execution_time:.6f}秒")



