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
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

json_str = '{"name": "Alice", "age": 18, "gender": "female"}'

def mysql_sync_impala(url,
                      username,
                      password,
                      source_table,
                      sink_table,
                      is_distributed, split_by):
    """
     mysql同步impala
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_cate: SRM、NORMAL、ROWID、INCRE、COL、QUERY、MysqlQuery
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info('mysql同步impala')

def oracle_sync_impala(url,
                       username,
                       password,
                       source_table,
                       sink_table,
                       sqoop_cate,
                       is_distributed, split_by):
    """
    oracle同步impala
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_cate: SRM、NORMAL、ROWID、INCRE、COL、QUERY、MysqlQuery
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("oracle同步impala")
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
    else:
        logger.info("未知sqoop抽数据类型!")

def postgresql_sync_impala(url,
                           username,
                           password,
                           source_table,
                           sink_table,
                           is_distributed, split_by):
    """
     postgresql同步impala
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_cate: SRM、NORMAL、ROWID、INCRE、COL、QUERY、MysqlQuery
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("postgresql同步impala")

def impala_sync_mysql(url,
                      username,
                      password,
                      source_table,
                      sink_table,
                      is_distributed, split_by):
    """
     impala同步mysql
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_cate: SRM、NORMAL、ROWID、INCRE、COL、QUERY、MysqlQuery
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("impala同步mysql")

def impala_sync_oracle(url,
                       username,
                       password,
                       source_table,
                       sink_table,
                       is_distributed, split_by):
    """
     impala同步oracle
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_cate: SRM、NORMAL、ROWID、INCRE、COL、QUERY、MysqlQuery
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("impala同步oracle")

def impala_sync_postgresql(url,
                           username,
                           password,
                           source_table,
                           sink_table,
                           is_distributed, split_by):
    """
     impala同步postgresql
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_cate: SRM、NORMAL、ROWID、INCRE、COL、QUERY、MysqlQuery
    :param is_distributed:
    :param split_by:
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
    pipeline_type = 'oracle_sync_impala'
    url = "jdbc:oracle:thin:@ebsdb-scan.kinwong.com:1531/prod"
    driver = ""
    username = "hadoop"
    password = "vSWnGLcdd8ch"
    source_table = ""
    sink_table = ""
    is_distributed = ""
    split_by = ""

    if pipeline_type == 'mysql_sync_impala':
        mysql_sync_impala(url,username,password,source_table,sink_table,is_distributed,split_by)
    elif pipeline_type == 'oracle_sync_impala':
        oracle_sync_impala(url,username,password,source_table,sink_table,is_distributed,split_by)
    elif pipeline_type == 'postgresql_sync_impala':
        postgresql_sync_impala(url,username,password,source_table,sink_table,is_distributed,split_by)
    elif pipeline_type == 'impala_sync_mysql':
        impala_sync_mysql(url,username,password,source_table,sink_table,is_distributed,split_by)
    elif pipeline_type == 'impala_sync_oracle':
        impala_sync_oracle(url,username,password,source_table,sink_table,is_distributed,split_by)
    elif pipeline_type == 'impala_sync_postgresql':
        impala_sync_postgresql(url,username,password,source_table,sink_table,is_distributed,split_by)
    else:
        logger.info("未知类型数据同步,请检查!")

    data = json.loads(json_str)

    # 获取姓名和年龄
    name = data['name']
    age = data['age']
    print(name)

    print(" >>> sqoop抽数结束!")