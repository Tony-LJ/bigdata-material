# -*- coding: utf-8 -*-
# ################################
# */5 * * * * /usr/bin/python3 /opt/project/prod_airflow_xunjian.py >> /opt/project/prod_airflow_xunjian.log 2>&1
#
# ###############################

import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"
# ##################

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

def get_dags(limit=100, offset=0):
    """
    获取DAG列表
    :param limit:
    :param offset:
    :return:
    """
    url = f"{AIRFLOW_URL}/dags"
    params = {"limit": limit, "offset": offset}

    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_list_dag_run(dag_id):
    """
    get_list_dag_run
    :param dag_id:
    :param limit:
    :param offset:
    :return:
    """

    url = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns"
    print(url)
    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_last_dagrun_task_instances(dag_id, run_id=None, limit=100):
    """
    获取任务实例列表
    :param dag_id:
    :param run_id:
    :param limit:
    :return:
    """
    if run_id:
        url = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns/{run_id}/taskInstances"
        print(url)
    else:
        url = f"{AIRFLOW_URL}/dags/{dag_id}/taskInstances"

    params = {"limit": limit}

    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def is_element_in_array(element, array):
    """
    判断元素是否在数组中
    :param element:
    :param array:
    :return:
    """
    return array.count(element) > 0

def get_csrf_token():
    session = requests.Session()
    # 第一步：获取 CSRF token
    login_page = session.get(f'http://10.53.0.75:8080/login')
    soup = BeautifulSoup(login_page.text, 'html.parser')

    # 提取 CSRF token
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    return csrf_token, session

def retryFailedTaskIdInDag(dag_id):
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
    failed_tasks =[]
    task_id = ''
    for taskInstance in taskInstances:
        task_id = taskInstance['task_id']
        state = taskInstance['state']
        print(f'{task_id}: {state}')
        # 如果任务状态为 failed，则记录下来
        if state == 'failed':
            failed_tasks.append(task_id)
            pass
        pass
        print("dag_id:{},last_dag_run_id:{},task_id:{},failed_tasks:{}".format(dag_id, last_dag_run_id, task_id, failed_tasks))
    execution_date = last_dag_run_id.split('__')[1]
    data = {
        'csrf_token': csrf_token,
        'dag_id': dag_id,
        'dag_run_id': last_dag_run_id,
        'task_id': task_id,
        'confirmed': 'true',
        'execution_date': execution_date
    }
    try:
        response = session.post(f'{AIRFLOW_URL}/clear',data=data, verify=False)
        # print(response.text)
    except:
        utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
        msg = "**DAG名称**: <font color='blue'>"+ dag_id + "</font>\n " + "**Task名称**: <font color='blue'>"+ task_id + "</font>\n" + "**执行日期**: <font color='blue'>"+ execution_date + "</font>\n" + "**异常原因**: <font color='blue'>"+ response.text + "</font>\n"
        send_wechat_work_message(utcWebhookUrl,msg)
        print("发现异常任务，但是巡检失败，请检查!", response.status_code, response.text)

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
    # dag_id = "utc_dag_id"
    # task_id = "utc_task_id"
    # execution_date = "2025-08-17"
    # content = "巡检测试消息"
    # utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
    # msg = "**DAG名称**: <font color='blue'>" + dag_id + "</font>\n " + "**Task名称**: <font color='blue'>" + task_id + "</font>\n" + "**执行日期**: <font color='blue'>" + execution_date + "</font>\n" + "**异常原因**: <font color='blue'>" + content + "</font>\n"
    # send_wechat_work_message(utcWebhookUrl,msg)
    csrf_token, session = get_csrf_token()
    print("airflow_csrf_token:{}, airflow_session:{}".format(csrf_token, session))
    print(" >>>>>> Airflow健康度检查" )
    health = get_airflow_health()
    if health:
        print(f"Metadatabase status: {health['metadatabase']['status']}")
        print(f"Scheduler status: {health['scheduler']['status']}")
        # print(f"Last scheduler heartbeat: {health['scheduler']['latest_heartbeat']}")

    print(" >>>>>> 获取DAG列表" )
    dags = get_dags(limit=50)
    active_dags = []
    # 指定需要额外处理的DAG
    prod_dags = ['kw_ods_dag_new','kw_dwd_dim_dag_new','kw_dws_ads_dag_new']

    if dags:
        print(f"Found {dags['total_entries']} DAGs")
        for dag in dags['dags']:
            # print(f"- {dag['dag_id']}: {'Paused' if dag['is_paused'] else 'Active'}")
            # 获取生效的DAG List
            if dag['is_active'] & is_element_in_array(dag['dag_id'], prod_dags):
                active_dags.append(dag['dag_id'])
    # print(active_dags)

    # 遍历指定DAG
    for active_dag in active_dags:
        retryFailedTaskIdInDag(active_dag)









