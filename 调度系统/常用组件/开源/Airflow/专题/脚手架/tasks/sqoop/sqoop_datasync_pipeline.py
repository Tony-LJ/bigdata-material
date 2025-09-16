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

def mysql_sync_impala(url,
                      username,
                      password,
                      source_table,
                      sink_table,
                      sqoop_type,
                      is_distributed, split_by, parallelism):
    """
     mysql同步impala
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_type: SRM、NORMAL、ROWID、INCRE、COL、QUERY
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info('mysql同步impala')
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def oracle_sync_impala(url,
                       username,
                       password,
                       source_table,
                       sink_table,
                       sqoop_type,
                       is_distributed, split_by, parallelism):
    """
    oracle同步impala
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_type: SRM、NORMAL、ROWID、INCRE、COL、QUERY
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("oracle同步impala")
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def postgresql_sync_impala(url,
                           username,
                           password,
                           source_table,
                           sink_table,
                           sqoop_type,
                           is_distributed, split_by, parallelism):
    """
     postgresql同步impala
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_type: SRM、NORMAL、ROWID、INCRE、COL、QUERY
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("postgresql同步impala")
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def impala_sync_mysql(url,
                      username,
                      password,
                      source_table,
                      sink_table,
                      sqoop_type,
                      is_distributed, split_by, parallelism):
    """
     impala同步mysql
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_type: SRM、NORMAL、ROWID、INCRE、COL、QUERY
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("impala同步mysql")
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def impala_sync_oracle(url,
                       username,
                       password,
                       source_table,
                       sink_table,
                       sqoop_type,
                       is_distributed, split_by, parallelism):
    """
     impala同步oracle
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_type: SRM、NORMAL、ROWID、INCRE、COL、QUERY
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("impala同步oracle")
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def impala_sync_postgresql(url,
                           username,
                           password,
                           source_table,
                           sink_table,
                           sqoop_type,
                           is_distributed, split_by, parallelism):
    """
     impala同步postgresql
    :param url:
    :param username:
    :param password:
    :param source_table:
    :param sink_table:
    :param sqoop_type: SRM、NORMAL、ROWID、INCRE、COL、QUERY
    :param is_distributed:
    :param split_by:
    :return:
    """
    logger.info("impala同步postgresql")
    if is_distributed == 0:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_cmd = f"""
        
        """
        os.system(sqoop_cmd)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def execute_sqoop_command(sqoop_command,sqoop_type, parallelism):
    """
    执行sqoop命令
    :param sqoop_command:
    :param sqoop_type: 同步类型:{SRM、NORMAL、ROWID、INCRE、COL、QUERY}
    :param parallelism: 任务并行度
    :return:
    """
    logger.info("执行sqoop命令...!")


json_str = '{"name": "Alice", "age": 18, "gender": "female"}'


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
    sqoop_type = ""
    sink_table = ""
    sqoop_cate = ""
    is_distributed = 1
    split_by = ""
    parallelism = 5

    # 判断sqoop数据同步类型
    if pipeline_type == 'mysql_sync_impala':
        mysql_sync_impala(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    elif pipeline_type == 'oracle_sync_impala':
        oracle_sync_impala(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    elif pipeline_type == 'postgresql_sync_impala':
        postgresql_sync_impala(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    elif pipeline_type == 'impala_sync_mysql':
        impala_sync_mysql(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    elif pipeline_type == 'impala_sync_oracle':
        impala_sync_oracle(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    elif pipeline_type == 'impala_sync_postgresql':
        impala_sync_postgresql(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    else:
        logger.info("未知类型数据同步,请检查!")

    # data = json.loads(json_str)
    # # 获取姓名和年龄
    # name = data['name']
    # age = data['age']
    # print(name)

    print(" >>> sqoop抽数结束!")