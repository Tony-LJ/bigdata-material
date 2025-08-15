# -*- coding: utf-8 -*-

"""
descr: Airflow系统交互

author: Tony
date: 2025-08-12
"""
import time

# import requests
# import json
#
# host = '10.53.0.75'
# port = '8080'
# user = 'airflow'
# password = 'airflow'
# baseUrl = 'http://' + host + ':' + port
# print(" >>> baseUrl: {}".format(baseUrl))
#
# headers = {
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'Connection': 'keep-alive',
#     'Origin': baseUrl,
#     'Referer': baseUrl + '/login',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
#     'accept': 'application/json, text/javascript, */*; q=0.01',
#     'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'x-requested-with': 'XMLHttpRequest',
# }
#
# # 登录请求接口
# loginUrl = baseUrl + '/login'
# print("loginUrl:{}".format(loginUrl))
#
# json_data = {
#     'username': user,
#     'password': password,
#     'validity': -1,
#     'sliderToken': '',
#     'origin': '',
#     'encrypted': True,
# }
# #. 登录获取accessToken
# session = requests.Session()
# response = session.post(loginUrl,
#                         headers=headers,
#                         json=json_data)
# # json 解析 response.content，获取accessToken
# data = json.loads(response.content)
# if response.status_code == 200 :
#     print('get accessToken success')
# else:
#     print('failed')
#     raise Exception('get accessToken failed')
# accessToken = data['data']['accessToken']
import requests
from requests.auth import HTTPBasicAuth

# 配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"

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

# 使用示例
dags = get_dags(limit=20)
if dags:
    print(f"Found {dags['total_entries']} DAGs")
    for dag in dags['dags']:
        print(f"- {dag['dag_id']}: {'Paused' if dag['is_paused'] else 'Active'}")


def trigger_dag_run(dag_id, run_id=None, conf=None):
    """
    触发DAG运行
    :param dag_id:
    :param run_id:
    :param conf:
    :return:
    """
    url = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns"

    data = {
        "dag_run_id": run_id or f"manual__{int(time.time())}",
        "conf": conf or {}
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 使用示例
run_config = {
    "param1": "value1",
    "param2": "value2"
}

result = trigger_dag_run(
    dag_id="kw_inv_stock_in_incr_d_dag",
    conf=run_config
)

if result:
    print(f"Triggered DAG run: {result['dag_run_id']}")
    print(f"Run URL: {result['url']}")


def update_dag_state(dag_id, is_paused):
    """
    更新DAG状态（暂停/恢复）
    :param dag_id:
    :param is_paused:
    :return:
    """
    url = f"{AIRFLOW_URL}/dags/{dag_id}?update_mask=is_paused"

    data = {
        "is_paused": is_paused
    }

    response = requests.patch(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 使用示例
# 暂停DAG
update_dag_state("my_data_pipeline", is_paused=True)

# 恢复DAG
update_dag_state("my_data_pipeline", is_paused=False)
