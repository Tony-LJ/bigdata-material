import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

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
api_url = f'{AIRFLOW_URL}/api/v1/dags/kw_dws_ads_dag_new/dagRuns'
response = session.get(api_url)
# 获取最新dagRuns
dag_runs = response.json()['dag_runs']
last_dag_run_id = dag_runs[-1]['dag_run_id']
# api_url = f'{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns/{last_dag_run_id}/taskInstances/{task_id}/dependencies'
api_url = f'{AIRFLOW_URL}/api/v1/dags/kw_guoshu_incr_day_dag/dagRuns/scheduled__2025-08-18T05:00:00+00:00/taskInstances/bi_ads_ads_device_lotnumtoebs_detail_ds/dependencies'
print(api_url)
response = session.get(api_url)
print(response)