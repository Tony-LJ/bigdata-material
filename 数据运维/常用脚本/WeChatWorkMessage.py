# -*- coding: utf-8 -*-
"""
descr: 企业微信机器人消息发送封装
author: tony
date: 2025-08-20
"""
import requests
import json


class WeChatWorkMessage:
    """
    descr 企业微信机器人消息发送模块
    """
    def send_wechat_work_message(webhook_url,
                                 content,
                                 mentioned_list=None):
        """
        发送企业微信机器人消息
        :param webhook_url: 机器人Webhook地址
        :param content: 要发送的文本内容
        :param mentioned_list: 需要@的成员列表(可选)
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or []
            }
        }

        try:
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            print("消息发送成功")
            return True
        except Exception as e:
            print(f"消息发送失败: {e}")
            return False

    def send_wechat_work_message(webhook_url,
                                 content,
                                 mentioned_list=None):
        """
        发送企业微信机器人消息
        :param webhook_url: 机器人Webhook地址
        :param content: 要发送的文本内容
        :param mentioned_list: 需要@的成员列表(可选)
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
                "mentioned_list": mentioned_list
            }
        }

        try:
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            print("消息发送成功")
            return True
        except Exception as e:
            print(f"消息发送失败: {e}")
            return False


if __name__ == '__main__':
    end_time = "异常"
    xunjian_team = "大数据团队"
    dag_base_info_error_arr = []
    utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
    msg = ("<font color='blue'> ** 巡检人员** </font> :  <font color='black'>**" + xunjian_team + "**</font>\n " +
           "<font color='blue'> **巡检日期** </font>: <font color='black'>**" + end_time + "**</font>\n " +
           "<font color='blue'> **异常DAG列表(执行时间>3小时)** </font> : \n <font color='black'>" + '\n'.join(dag_base_info_error_arr) + "</font>\n ")
    WeChatWorkMessage.send_wechat_work_message(utcWebhookUrl,msg)
