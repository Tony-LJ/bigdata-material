# -*- coding: utf-8 -*-
"""
descr: 企业微信机器人消息发送封装
author: tony
date: 2025-08-20
"""
import base64
import hashlib
import os

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

    def send_message_to_wechat02(webhook_url):
        markdown_content = f"""
        **实时通知** <font color="warning">请注意</font>！
        ---
        > 任务状态：<font color="info ">进行中</font> 
        > 负责人：<u><@Pyhton></u>  <font color="#008000">请跟进处理</font>
        >请相关同事注意跟进。
        """
        # 要发送的消息内容
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": markdown_content,
                # Markdown 消息中 @ 成员需要直接在 content 中写入 <@userid>
            },
        }
        # 发送POST请求
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        # 打印响应结果
        print(response.text)

    # 企业微信机器人发送数据
    def send_message_to_wechat(webhook_url):
        send_message = f"Hello~\n\n自动通报信息的机器人，已启动工作！\n"
        data = {
            "msgtype": "text",  # 消息类型：文本
            "text": {
                "content": send_message,  # 消息内容
                "mentioned_list": ["@all"],  # @所有人，如果需要的话
            },
        }
        # 发送POST请求
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        # 打印响应结果
        print(response.text)


    def send_image_to_wechat(webhook_url, image_path):
        # 2. 读取图片 -> Base64 编码 -> 计算 MD5
        with open(image_path, "rb") as f:
            image_data = f.read()
            # 编码后需要解码为 utf-8 字符串
            base64_data = base64.b64encode(image_data).decode("utf-8")
            md5_hash = hashlib.md5(image_data).hexdigest()

        # 3. 构建请求数据（图片类型）
        data = {"msgtype": "image", "image": {"base64": base64_data, "md5": md5_hash}}

        # 4. 设置请求头
        headers = {"Content-Type": "application/json"}

        # 5. 发送 POST 请求
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    def send_news_to_wechat(webhook_url, image_path):
        # 1. 构建请求数据（图文类型）
        data = {
            "msgtype": "news",
            "news": {
                "articles": [  # 最多支持 8 条图文
                    {
                        "title": "中秋节礼品领取",
                        "description": "系统将于今晚 22:00 - 24:00 进行升级维护...",
                        "url": "http://example.com/announcement/123",
                        "picurl": "头像.JPG",
                    },
                    {
                        "title": "我是Python伍六七",
                        "description": "点击查看详细报告内容",
                        "url": "https://mp.weixin.qq.com/s/VW32gkrk0U38UG86milE9Q",
                        "picurl": "http://res.example.com/images/report_icon.png",
                    },
                ]
            },
        }
        # 2. 设置请求头
        headers = {"Content-Type": "application/json"}
        # 3. 发送 POST 请求
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    def send_file_to_wechat(upload_url, send_url, file_path):
        # 此url目的为：获取文件media_id
        upload_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=xxxxxx&type=file"      # 此url目的为：获取文件media_idsend_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?xxxxxx"
        # 1. 上传文件获取media_id
        file_name = os.path.basename(file_path)  # 从路径提取文件名
        with open(file_path, "rb") as f:
            # 注意字段名必须是"media"
            response = requests.post(upload_url, files={"media": (file_name, f)})
            response_data = response.json()
            media_id = response_data.get("media_id")

        # 2.构建请求数据（文件类型）
        payload = {"msgtype": "file", "file": {"media_id": media_id}}
        # 3.设置请求头
        headers = {"Content-Type": "application/json"}
        # 4. 发送 POST 请求
        response = requests.post(send_url, data=json.dumps(payload), headers=headers)



if __name__ == '__main__':
    end_time = "异常"
    xunjian_team = "大数据团队"
    dag_base_info_error_arr = []
    utcWebhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
    msg = ("<font color='blue'> ** 巡检人员** </font> :  <font color='black'>**" + xunjian_team + "**</font>\n " +
           "<font color='blue'> **巡检日期** </font>: <font color='black'>**" + end_time + "**</font>\n " +
           "<font color='blue'> **异常DAG列表(执行时间>3小时)** </font> : \n <font color='black'>" + '\n'.join(dag_base_info_error_arr) + "</font>\n ")
    # WeChatWorkMessage.send_wechat_work_message(utcWebhookUrl,msg)
    WeChatWorkMessage.send_message_to_wechat02(utcWebhookUrl) # 相关
