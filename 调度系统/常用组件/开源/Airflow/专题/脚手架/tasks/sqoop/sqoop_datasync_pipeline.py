# -*- coding: utf-8 -*-
"""
descr : Sqoop抽数脚手架
auther : lj.michale
create_date : 2025/9/19 15:54
file_name : sqoop_datasync_pipeline.py
"""
import json

json_str = '{"name": "Alice", "age": 18, "gender": "female"}'


if __name__ == '__main__':
    print(" >>> sqoop抽数开始!")
    data = json.loads(json_str)

    # 获取姓名和年龄
    name = data['name']
    age = data['age']
    print(name)

    print(" >>> sqoop抽数结束!")