# -*- coding: utf-8 -*-
"""
descr : Sqoop抽数脚手架
auther : lj.michale
create_date : 2025/9/19 15:54
file_name : sqoop_datasync_pipeline.py
"""
import json
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

json_str = '{"name": "Alice", "age": 18, "gender": "female"}'

def mysql_sync_impala(url,
                      driver,
                      username,
                      password,
                      is_distributed,split_by ):
    """
     mysql同步impala
    :param url:
    :param driver:
    :param username:
    :param password:
    :return:
    """
    logger.info('mysql同步impala')

def oracle_sync_impala(url,
                       driver,
                       username,
                       password,
                       is_distributed,split_by):
    """
     oracle同步impala
    :param url:
    :param driver:
    :param username:
    :param password:
    :return:
    """
    logger.info("oracle同步impala")

def postgresql_sync_impala(url,
                           driver,
                           username,
                           password,
                           is_distributed,split_by):
    """
     postgresql同步impala
    :param url:
    :param driver:
    :param username:
    :param password:
    :return:
    """
    logger.info("postgresql同步impala")

def impala_sync_mysql(url,
                      driver,
                      username,
                      password,
                      is_distributed,split_by):
    """
     impala同步mysql
    :param url:
    :param driver:
    :param username:
    :param password:
    :return:
    """
    logger.info("impala同步mysql")

def impala_sync_oracle(url,
                       driver,
                       username,
                       password,
                       is_distributed,split_by):
    """
     impala同步oracle
    :param url:
    :param driver:
    :param username:
    :param password:
    :return:
    """
    logger.info("impala同步oracle")

def impala_sync_postgresql(url,
                           driver,
                           username,
                           password,
                           is_distributed,split_by):
    """
     impala同步postgresql
    :param url:
    :param driver:
    :param username:
    :param password:
    :return:
    """
    logger.info("impala同步postgresql")


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='请传入Sqoop抽数脚本所需必要参数!')
    # # parser = argparse.ArgumentParser(description='manual to this script')
    # parser.add_argument("–gpus", type=str, default="0")
    # parser.add_argument("–batch-size", type=int, default=32)
    # args = parser.parse_args()
    # print(args.gpus)
    # print(args.batch_size)

    print(" >>> sqoop抽数开始!")
    pipeline_type = 'mysql_sync_impala'

    if pipeline_type == 'mysql_sync_impala':
        print("mysql同步impala")
    elif pipeline_type == 'oracle_sync_impala':
        print("oracle同步impala")
    elif pipeline_type == 'postgresql_sync_impala':
        print("postgresql同步impala")
    elif pipeline_type == 'impala_sync_mysql':
        print("impala同步mysql")
    elif pipeline_type == 'impala_sync_oracle':
        print("impala同步oracle")
    elif pipeline_type == 'impala_sync_postgresql':
        print("impala同步postgresql")
    else:
        print("未知类型数据同步!")

    data = json.loads(json_str)

    # 获取姓名和年龄
    name = data['name']
    age = data['age']
    print(name)

    print(" >>> sqoop抽数结束!")