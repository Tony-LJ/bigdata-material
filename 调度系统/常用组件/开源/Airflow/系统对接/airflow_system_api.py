# -*- coding: utf-8 -*-

"""
descr: airflow api系统交互脚本
author: tony
date: 2025-08-12
"""
import os
import time
import requests
from requests.auth import HTTPBasicAuth

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"
# ##################

# ################## DAG管理
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

# ################## Task任务实例管理
def get_task_instances(dag_id, run_id=None, limit=100):
    """
    获取任务实例列表
    :param dag_id:
    :param run_id:
    :param limit:
    :return:
    """
    if run_id:
        url = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns/{run_id}/taskInstances"
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

def clear_task_instances(dag_id, start_date, end_date, task_ids=None):
    """
    清除指定日期范围内的任务实例状态
    :param dag_id:
    :param start_date:
    :param end_date:
    :param task_ids:
    :return:
    """
    url = f"{AIRFLOW_URL}/dags/{dag_id}/clearTaskInstances"

    data = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "task_ids": task_ids or [],
        "only_failed": False,
        "only_running": False
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# ################## 连接管理
def create_connection(conn_id, conn_type, host, login, password, port=None, extra=None):
    """
    创建Airflow连接
    :param conn_id:
    :param conn_type:
    :param host:
    :param login:
    :param password:
    :param port:
    :param extra:
    :return:
    """
    url = f"{AIRFLOW_URL}/connections"

    data = {
        "connection_id": conn_id,
        "conn_type": conn_type,
        "host": host,
        "login": login,
        "password": password,
        "port": port,
        "extra": extra or "{}"
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

# ################## 变量管理
def set_variable(key, value):
    """设置Airflow变量"""
    url = f"{AIRFLOW_URL}/variables/{key}"

    data = {
        "key": key,
        "value": value
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

def get_variable(key):
    """获取Airflow变量"""
    url = f"{AIRFLOW_URL}/variables/{key}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()["value"]
    elif response.status_code == 404:
        print(f"Variable {key} not found")
        return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# ################## 批量触发DAG
def batch_trigger_dags(dag_ids, conf=None):
    """
    批量触发多个DAG
    :param dag_ids:
    :param conf:
    :return:
    """
    url = f"{AIRFLOW_URL}/dags/~/dagRuns/list"

    data = {
        "dag_runs": [
            {
                "dag_id": dag_id,
                "dag_run_id": f"batch_manual__{int(time.time())}_{i}",
                "conf": conf or {}
            } for i, dag_id in enumerate(dag_ids)
        ]
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# ################## 监控Airflow健康状态
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


# ################## 构建DAG部署流水线
def deploy_dag(dag_file_path):
    """
    部署DAG文件到Airflow：结合Git和CI/CD工具，使用API实现DAG自动部署
    :param dag_file_path:
    :return:
    """
    # 读取DAG文件内容
    with open(dag_file_path, 'r') as f:
        dag_content = f.read()

    # 获取文件名
    dag_file_name = os.path.basename(dag_file_path)

    # Airflow的DAGs文件夹API端点（需要启用Webhdfs或类似服务）
    # 实际部署可能需要结合Airflow的DAG同步机制
    url = f"{AIRFLOW_URL}/dags/import"

    data = {
        "file_name": dag_file_name,
        "content": dag_content
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def safe_api_call(func, *args, **kwargs):
    """
    安全调用API的装饰器
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    max_retries = 3
    retry_delay = 2  # 秒

    for attempt in range(max_retries):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"API调用失败 (尝试 {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

    print("达到最大重试次数，API调用失败")
    return None


if __name__ == '__main__':
    print(" >>>>>> Airflow健康度检查" )
    health = get_airflow_health()
    if health:
        print(f"Metadatabase status: {health['metadatabase']['status']}")
        print(f"Scheduler status: {health['scheduler']['status']}")
        # print(f"Last scheduler heartbeat: {health['scheduler']['latest_heartbeat']}")









