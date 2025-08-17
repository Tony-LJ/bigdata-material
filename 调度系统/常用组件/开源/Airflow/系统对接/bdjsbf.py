# -*- coding: utf-8 -*-

import os
import time
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# ################## 基础信息配置
AIRFLOW_URL = "http://10.53.0.75:8080"
USERNAME = "airflow"
PASSWORD = "airflow"



