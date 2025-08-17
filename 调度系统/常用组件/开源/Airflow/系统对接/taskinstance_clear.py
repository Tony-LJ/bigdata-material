# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080"
USERNAME = "airflow"
PASSWORD = "airflow"
# ##################

dag_id = 'kw_guoshu_incr_day_dag'

# 创建会话
session = requests.Session()

# 第一步：获取 CSRF token
login_page = session.get(f'{AIRFLOW_URL}/login')
soup = BeautifulSoup(login_page.text, 'html.parser')

# 提取 CSRF token
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
print("csrf_token:{}".format(csrf_token))

# 用户凭据
credentials = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrf_token': csrf_token  # 添加 CSRF token
}

# 第二步：登录请求
response = session.post(f'{AIRFLOW_URL}/login', data=credentials)
# 调用 API 端点
# 获取dag列表
api_url = f'{AIRFLOW_URL}/api/v1/dags'
response = session.get(api_url)
# 获取指定dag的信息
api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns'
response = session.get(api_url)

# 获取最新dagRuns
dag_runs = response.json()['dag_runs']
last_dag_run_id = 'scheduled__2025-08-16T05:00:00+00:00'

# 检查登录是否成功
if response.ok:
    print("登录成功")
else:
    print("登录失败:", response.status_code, response.text)

# 获取任务状态
api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns/{last_dag_run_id}/taskInstances'
print(api_url)
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

execution_date = last_dag_run_id.split('__')[1]
print(execution_date)

data = {
    'csrf_token': csrf_token,
    'dag_id': dag_id,
    'dag_run_id': last_dag_run_id,
    'task_id': task_id,
    'confirmed': 'true',
    'execution_date': execution_date
}


response = session.post(f'{AIRFLOW_URL}/clear',data=data, verify=False)

