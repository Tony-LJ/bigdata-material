# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def retry_failed_taskInstance_InDag(dag_id):
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
    print(api_url)
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
    print("dag_id:{},task_id:{},failed_tasks:{}".format(dag_id, task_id, failed_tasks))
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
        print("发现异常任务，但是巡检失败，请检查!", response.status_code, response.text)
if __name__ == '__main__':
    print(">>>>>Airflow DAG失败Task实例巡检开始")
    retry_failed_taskInstance_InDag("kw_guoshu_incr_day_dag")






