# -*- coding: utf-8 -*-

import os
import time
import datetime
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"
# ##################

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
        "only_failed": True,
        "only_running": False
    }

    print(url)
    print(data)

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        print("返回值:{}".format(response.json()))
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 使用示例
from datetime import datetime, timedelta
import pytz

start = datetime.now().now(pytz.utc) - timedelta(days=1)
end = datetime.now().now(pytz.utc) + timedelta(days=1)

clear_task_instances(
    dag_id="kw_guoshu_incr_day_dag",
    start_date=start,
    end_date=end,
    task_ids=["bi_ads_ads_device_lotnumtoebs_detail_ds"]
)
