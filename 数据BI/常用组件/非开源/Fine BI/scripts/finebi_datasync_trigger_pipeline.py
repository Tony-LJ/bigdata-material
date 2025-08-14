# -*- coding: utf-8 -*-

"""
Descr: Fine BI 数据同步触发脚本

Author: Tony
Date: 2025-08-12
"""

import requests
import json
import sys


# 读取 py脚本外接参数 ,第一个参数是表名；第二个参数是抽取类型，没有则默认为1
table_name = sys.argv[1]
updateType = sys.argv[2] if len(sys.argv)>1 else '1'


