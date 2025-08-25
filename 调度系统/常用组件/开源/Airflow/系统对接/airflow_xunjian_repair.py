# -*- coding: utf-8 -*-
# ################################
# */10 * * * * /usr/bin/python3 /opt/project/airflow_xunjian_repair.py >> /opt/project/airflow_xunjian_repair.log 2>&1
#
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

# def query_impala_bysql(sql):
#     """
#     查询impala
#     :param sql:
#     :return:
#     """
#     conn = connect(host='10.53.0.71',
#                    port=21050,
#                    user="root",
#                    password="",
#                    database="impala")
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     meta_lst = cursor.fetchall()
#     print(meta_lst)
#     cursor.close()
#     return meta_lst

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
    for taskInstance in taskInstances:
        task_id = taskInstance['task_id']
        state = taskInstance['state']
        print(f'{task_id}: {state}')
        # 如果任务状态为 failed，则记录下来
        if state == 'failed':
            failed_tasks.append(task_id)
            pass
        pass
        # print("dag_id:{},last_dag_run_id:{},task_id:{},failed_tasks:{}".format(dag_id, last_dag_run_id, task_id, failed_tasks))
    execution_date = last_dag_run_id.split('__')[1]
    # 无异常任务时
    if len(failed_tasks) == 0:
        struct_time = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        print(">>>>>无异常任务,巡检时间:{}".format(current_time))
        # utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
        # msg = "**DAG巡检结果**: <font color='blue'> " + dag_id + "无异常任务,巡检日期:" + current_time + " </font>\n "
        # send_wechat_work_message(utcWebhookUrl,msg)
    else:
        # 存在异常任务时
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
                # 同步更新FineBI,bi_ads_ads_kwhrsys_avw_attend_day_hadoop_pme_ds.sql
                # table_name = task_id[7:][:-4]
                # print("推送表:{} 数据到FineBI".format(table_name))
                # # bi_data.dwd_finebi_info_ds属于T+1更新
                # sql = "select script_name,table_name,table_id,update_type from bi_data.dwd_finebi_info_ds where table_name = " + "'" + table_name + "'"
                # table_id = query_impala_bysql(sql)[0][2]
                # update_data_to_finebi(table_id,2)
            except:
                utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
                msg = "**DAG名称**: <font color='blue'>" + dag_id + "</font>\n " + "**Task名称**: <font color='blue'>" + task_id + "</font>\n" + "**执行日期**: <font color='blue'>" + execution_date + "</font>\n" + "**异常原因**: <font color='blue'>" + response.text + "</font>\n"
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

def update_data_to_finebi(table_name, update_type):
    """
    更新FineBI的数据
    :param table_name:
    :param update_type:
    :return:
    """
    fineBiUrl = 'http://10.53.1.173:8080'
    session = requests.Session()
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Origin': fineBiUrl,
        'Referer': fineBiUrl + '/decision/login',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-requested-with': 'XMLHttpRequest',
    }
    json_data = {
        'username': '000000',
        'password': 'PddHSuNXLHRl7etM2DZ5kg==',
        'validity': -1,
        'sliderToken': '',
        'origin': '',
        'encrypted': True,
    }
    response = session.post(fineBiUrl + '/decision/login', headers=headers, json=json_data)
    data = json.loads(response.content)
    if response.status_code == 200 :
        print('get accessToken success')
    else:
        print('failed')
        raise Exception('get accessToken failed')
    accessToken = data['data']['accessToken']
    cookies = {
        'tenantId': 'default',
        'fine_remember_login': '-1',
        'dev': 'UqNTp725yS2lMBaBDPL3WY7tLd',
        'fine_login_users': 'f-9200302300158213064,4340becf-ca56-4f60-b9f9-653c8a47a02a',
        'fine_auth_token': accessToken,
    }
    json_data = {
        'updateType': update_type,
        'tableName': table_name,
    }
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Origin': fineBiUrl,
        'Referer': fineBiUrl + '/decision',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer '+accessToken,
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sessionid': '503e40ccf5d5ec9c',
        'x-requested-with': 'XMLHttpRequest',
    }
    response = session.post(fineBiUrl + '/decision/v5/conf/update/tables/' + table_name + '/trigger', cookies=cookies, headers=headers, json=json_data)
    data = json.loads(response.content)
    if data['code'] == '200':
        print('success')
    else:
        print('failed')
        raise Exception('failed')

# def get_taskid_dependencies(dag_id, task_id):
#     """
#     获取指定DAG Task ID的前后依赖关系
#     :param dag_id:
#     :param task_id:
#     :return:
#     """
#     AIRFLOW_URL = "http://10.53.0.75:8080"
#     USERNAME = "airflow"
#     PASSWORD = "airflow"
#     session = requests.Session()
#     login_page = session.get(f'{AIRFLOW_URL}/login')
#     soup = BeautifulSoup(login_page.text, 'html.parser')
#     csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
#     print("csrf_token:{}".format(csrf_token))
#     credentials = {
#         'username': USERNAME,
#         'password': PASSWORD,
#         'csrf_token': csrf_token  # 添加 CSRF token
#     }
#     response = session.post(f'{AIRFLOW_URL}/login', data=credentials)
#     api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns'
#     response = session.get(api_url)
#     # 获取最新dagRuns
#     dag_runs = response.json()['dag_runs']
#     last_dag_run_id = dag_runs[-1]['dag_run_id']
#     # api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns/{last_dag_run_id}/taskInstances/{task_id}/dependencies'
#     api_url = f'{AIRFLOW_URL}/api/v1/dags/kw_guoshu_incr_day_dag/dagRuns/scheduled__2025-08-18T05:00:00+00:00/taskInstances/bi_data_dwd_cux_cux_lotnumtoebs_t/dependencies'
#     response = session.get(api_url)
#     print(response.text)


if __name__ == '__main__':
    # get_taskid_dependencies("kw_dws_ads_dag_new", "bi_ads_ads_oa_equip_accept_report_ds.sql")
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
    prod_dags = ['kw_dws_ads_dag_new']

    if dags:
        # print(f"Found {dags['total_entries']} DAGs")
        for dag in dags['dags']:
            # print(f"- {dag['dag_id']}: {'Paused' if dag['is_paused'] else 'Active'}")
            # 获取生效的DAG List
            if dag['is_active'] & is_element_in_array(dag['dag_id'], prod_dags):
                active_dags.append(dag['dag_id'])
    # print(active_dags)

    # 遍历指定DAG
    for active_dag in active_dags:
        retryFailedTaskIdInDag(active_dag)





