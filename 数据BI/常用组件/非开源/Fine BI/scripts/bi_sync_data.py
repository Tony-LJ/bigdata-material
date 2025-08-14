""" 
================================================
# author: chen liu
# purpose : 同步抽取BI数据
# create_at : 2024-12-25
========================================================

========================================================


"""


import requests
import json
import sys

# Absolute path to your kw_airflow_utils.py
kw_utils_path = "/root/airflow/dags" # Adjust if needed

# Add the directory to the PYTHONPATH
sys.path.append(kw_utils_path)

from kw_airflow_utils import KwUtils # or from kw_airflow_utils import KwUtils if it's a class


#1. 读取配置文件
ini_path =  kw_utils_path + "/profile_kw.ini"
impala_ini = KwUtils.config_read_ini("BI", ini_path)
host = impala_ini[0]
port = impala_ini[1]
user = impala_ini[2]
password = impala_ini[3]
origin = 'http://'+host+':'+port

# 读取 py脚本外接参数 ,第一个参数是表名；第二个参数是抽取类型，没有则默认为1
table_name = sys.argv[1]
updateType = sys.argv[2] if len(sys.argv)>1 else '1'

#2. 登录获取accessToken
session = requests.Session()

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': origin,
    'Referer': origin+'/decision/login',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-requested-with': 'XMLHttpRequest',
}

json_data = {
    'username': user,
    'password': password,
    'validity': -1,
    'sliderToken': '',
    'origin': '',
    'encrypted': True,
}

response = session.post(origin+'/decision/login', headers=headers, json=json_data)

#json 解析 response.content，获取accessToken
data = json.loads(response.content)
print(data)
if response.status_code == 200 :
    print('get accessToken success')
else:
    print('failed')
    raise Exception('get accessToken failed')
accessToken = data['data']['accessToken']


#3. 开始同步抽取数据

cookies = {
    'tenantId': 'default',
    'fine_remember_login': '-1',
    'dev': 'UqNTp725yS2lMBaBDPL3WY7tLd',
    'fine_login_users': 'f-9200302300158213064,4340becf-ca56-4f60-b9f9-653c8a47a02a',
    'fine_auth_token': accessToken,

}

json_data = {
    'updateType': updateType,
    'tableName': table_name,
}

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': origin,
    'Referer': origin+'/decision',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'accept': 'application/json, text/plain, */*',
    'authorization': 'Bearer '+accessToken,
    'content-type': 'application/json;charset=UTF-8',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sessionid': '503e40ccf5d5ec9c',
    'x-requested-with': 'XMLHttpRequest',
}

response = session.post(origin+'/decision/v5/conf/update/tables/'+table_name+'/trigger', cookies=cookies, headers=headers, json=json_data)
print(response.content)

#解析response.content 提取 code
#try except 如果返回的不是200 则失败
data = json.loads(response.content)
if data['code'] == '200':
    print('success')
else:
    print('failed')
    raise Exception('failed')