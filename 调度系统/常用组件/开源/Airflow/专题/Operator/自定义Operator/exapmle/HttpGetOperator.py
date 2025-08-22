# -*- coding: utf-8 -*-
"""
descr: 自定义Operator的示例，该Operator用于执行一个简单的HTTP GET请求：
author: tony
date: 2025-08-20
"""
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests

class HttpGetOperator(BaseOperator):
    @apply_defaults
    def __init__(self, endpoint, params=None, *args, **kwargs):
        super(HttpGetOperator, self).__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.params = params or {}

    def execute(self, context):
        response = requests.get(self.endpoint, params=self.params)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
        self.log.info(f"HTTP GET request to {self.endpoint} succeeded with status code {response.status_code}")
        return response.json()  # 假设返回的是JSON格式的数据

