# -*- coding: utf-8 -*-

"""
descr: Fine BI 数据同步触发脚本
author: Tony
date: 2025-08-12
"""

import requests
import json

host = '10.53.1.173'
port = '8080'
user = '000000'
password = 'PddHSuNXLHRl7etM2DZ5kg=='
baseUrl = 'http://' + host + ':' + port
print("baseUrl:{}".format(baseUrl))

# ###################模拟登陆
#. 登录获取accessToken
session = requests.Session()
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': baseUrl,
    'Referer': baseUrl + '/decision/login',
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

# 登录请求接口
loginUrl = baseUrl + '/decision/login'
print("loginUrl:{}".format(loginUrl))

response = session.post(loginUrl,
                        headers=headers,
                        json=json_data)
# json 解析 response.content，获取accessToken
data = json.loads(response.content)
if response.status_code == 200 :
    print('get accessToken success')
else:
    print('failed')
    raise Exception('get accessToken failed')
accessToken = data['data']['accessToken']

# ##################################################### 模拟成功登录之后的操作
table_name = '8fecd8cae2454e5d8cef41f3ea14cf40'
updateType = '2'

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
    'Origin': baseUrl,
    'Referer': baseUrl + '/decision',
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

# 数据同步更新接口
dataSyncTriggerUrl = baseUrl + '/decision/v5/conf/update/tables/'+table_name+'/trigger'
print("dataSyncTriggerUrl:{}".format(dataSyncTriggerUrl))
response = session.post(dataSyncTriggerUrl,
                        cookies=cookies,
                        headers=headers,
                        json=json_data)
# 解析response.content 提取 code
# try except 如果返回的不是200 则失败
data = json.loads(response.content)
if data['code'] == '200':
    print('success')
else:
    print('failed')
    raise Exception('failed')
