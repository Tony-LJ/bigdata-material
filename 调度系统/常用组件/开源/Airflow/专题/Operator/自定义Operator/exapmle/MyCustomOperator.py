# -*- coding: utf-8 -*-
"""
descr: 自定义Operator的示例
author: tony
date: 2025-08-20
"""
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests

class MyCustomOperator(BaseOperator):
    """
    自定义Operator的示例
    """
    @apply_defaults
    def __init__(self, some_arg, *args, **kwargs):
        super(MyCustomOperator, self).__init__(*args, **kwargs)
        self.some_arg = some_arg

    def execute(self, context):
        """
        执行任务的具体逻辑
        """
        print(f"Executing MyCustomOperator with arg: {self.some_arg}")
        # 在这里添加你的任务逻辑，例如调用API、处理文件等

    def on_kill(self):
        """
        当任务被杀死时执行的方法（可选）
        """
        print("MyCustomOperator is being killed")