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

def oracle_sync_impala(jdbc_url,
                       username,
                       password,
                       source_table,
                       sink_table,
                       sqoop_type,
                       is_distributed, split_by, parallelism):
    """
     oracle同步impala
    :param jdbc_url:
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
        sqoop_command = f"""
        
        """
        # execute_sqoop_command(sqoop_type)
        logger.info("开始常规抽数")
    elif is_distributed == 1:
        sqoop_command = f"""
        
        """
        os.system(sqoop_command)
        logger.info("开始分布式抽数")
    else:
        logger.info("未知sqoop抽数据类型!")

def execute_sqoop_command(jdbc_url,
                          username,
                          source_table,
                          sink_table,
                          password,
                          sqoop_type,sqoop_param):
    """
    执行sqoop数据同步抽数命令
    :param jdbc_url:
    :param username:
    :param source_table:
    :param sink_table:
    :param password:
    :param sqoop_type: 同步类型:{SRM、NORMAL、ROWID、INCRE、COL、QUERY}
    :param sqoop_param: sqoop参数列
    :return:
    """
    logger.info("执行sqoop命令...!")
    if sqoop_type == "NORMAL":
        # sqoop import --connect jdbc:oracle:thin:@192.168.0.50:1521/kwmi --username HADOOP --password sd!GI8*7 --table MDMUSER.WLZ --hive-import --hive-database bi_ods --hive-table ODS_MDMUSER_WLZ --delete-target-dir --hive-drop-import-delims --fields-terminated-by '\001' --lines-terminated-by '\n' --null-string '\\N' --null-non-string '\\N' --hive-overwrite --m 1
        sqoop_command = f"""
        sqoop import \
        --connect {jdbc_url} \
        --username {username} \
        --password {password} \
        --table {source_table} \
        --hive-import \
        --hive-database bi_ods \
        --hive-table {sink_table} \
        --delete-target-dir \
        --hive-drop-import-delims \
        --fields-terminated-by '\\001' \
        --lines-terminated-by '\\n' \
        --null-string '\\\\N' \
        --null-non-string '\\\\N' \
        --hive-overwrite \
        --m 1
        """
        logger.info("常规NORMAL抽数,SQOOP执行命令:{}".format(sqoop_command))
        os.system(sqoop_command)
    elif sqoop_type == "ROWID":
        # sqoop import --connect jdbc:oracle:thin:@ebsdb-scan.kinwong.com:1531/prod --username hadoop --password vSWnGLcdd8ch --table APPS.CUX_INV_RIGHT_V --hive-import --hive-database bi_ods --hive-table ODS_APPS_CUX_INV_RIGHT_V --delete-target-dir --hive-drop-import-delims --fields-terminated-by '\001' --lines-terminated-by '\n' --null-string '\\N' --null-non-string '\\N' --map-column-java ROW_ID=String  --map-column-hive ROW_ID=String   --hive-overwrite --m 1
        sqoop_command = f"""
        sqoop import \
        --connect {jdbc_url} \
        --username {username} \
        --password {password} \
        --table {source_table} \
        --hive-import \
        --hive-database bi_ods \
        --hive-table {sink_table} \
        --delete-target-dir \
        --hive-drop-import-delims \
        --fields-terminated-by '\\001' \
        --lines-terminated-by '\\n' \
        --null-string '\\\\N' \
        --null-non-string '\\\\N' \
        --map-column-java {sqoop_param}  \
        --map-column-hive {sqoop_param}   \
        --hive-overwrite \
        --m 1
        """
        logger.info("特殊类型ROWID抽数(指定列抽数),SQOOP执行命令:{}".format(sqoop_command))
        os.system(sqoop_command)
    elif sqoop_type == "INCRE":
        #  sqoop import --connect jdbc:oracle:thin:@192.168.0.50:1521/ehr --username hadoop --password KW34hadop --target-dir /sqoop/conditiontest/ODS_KWHRSYS_AVW_ATTEND_DAY_HADOOP --delete-target-dir --query "select * from KWHRSYS.AVW_ATTEND_DAY_HADOOP where  term >= sysdate-60   and \$CONDITIONS " --hive-import --hive-database bi_ods --hive-table ODS_KWHRSYS_AVW_ATTEND_DAY_HADOOP --hive-drop-import-delims --fields-terminated-by '\001' --lines-terminated-by '\n' --null-string '\\N' --null-non-string '\\N' --hive-overwrite --m 1
        sqoop_command = f"""
        sqoop import \
        --connect {jdbc_url} \
        --username {username} \
        --password {password} \
        --target-dir /sqoop/conditiontest/{sink_table} \
        --delete-target-dir \
        --query "select * from {source_table} where  {sqoop_param}   and \\$CONDITIONS " \
        --hive-import \
        --hive-database bi_ods \
        --hive-table {sink_table} \
        --hive-drop-import-delims \
        --fields-terminated-by '\\001' \
        --lines-terminated-by '\\n' \
        --null-string '\\\\N' \
        --null-non-string '\\\\N' \
        --hive-overwrite \
        --m 1
        """
        logger.info("INCRE抽数(增量抽数),SQOOP执行命令:{}".format(sqoop_command))
        os.system(sqoop_command)
    elif sqoop_type == "COL":
        # sqoop import --connect jdbc:oracle:thin:@ebsdb-scan.kinwong.com:1531/prod --username hadoop --password vSWnGLcdd8ch --table APPS.WIP_DISCRETE_JOBS_V --hive-import --hive-database bi_ods --hive-table ODS_APPS_WIP_DISCRETE_JOBS_V --delete-target-dir --hive-drop-import-delims --fields-terminated-by '\001' --lines-terminated-by '\n' --null-string '\\N' --null-non-string '\\N' --columns WIP_ENTITY_ID,WIP_ENTITY_NAME,ORGANIZATION_ID,LAST_UPDATE_DATE,LAST_UPDATED_BY,CREATION_DATE,CREATED_BY,LAST_UPDATE_LOGIN,REQUEST_ID,PROGRAM_APPLICATION_ID,PROGRAM_ID,PROGRAM_UPDATE_DATE,DESCRIPTION,STATUS_TYPE,PRIMARY_ITEM_ID,FIRM_PLANNED_FLAG,JOB_TYPE,JOB_TYPE_MEANING,WIP_SUPPLY_TYPE,CLASS_CODE,MATERIAL_ACCOUNT,MATERIAL_OVERHEAD_ACCOUNT,RESOURCE_ACCOUNT,OUTSIDE_PROCESSING_ACCOUNT,MATERIAL_VARIANCE_ACCOUNT,RESOURCE_VARIANCE_ACCOUNT,OUTSIDE_PROC_VARIANCE_ACCOUNT,STD_COST_ADJUSTMENT_ACCOUNT,OVERHEAD_ACCOUNT,OVERHEAD_VARIANCE_ACCOUNT,SCHEDULED_START_DATE,DATE_RELEASED,SCHEDULED_COMPLETION_DATE,DATE_COMPLETED,DATE_CLOSED,START_QUANTITY,QUANTITY_REMAINING,QUANTITY_COMPLETED,QUANTITY_SCRAPPED,NET_QUANTITY,BOM_REFERENCE_ID,ROUTING_REFERENCE_ID,COMMON_BOM_SEQUENCE_ID,COMMON_ROUTING_SEQUENCE_ID,BOM_REVISION,ROUTING_REVISION,BOM_REVISION_DATE,ROUTING_REVISION_DATE,LOT_NUMBER,ALTERNATE_BOM_DESIGNATOR,ALTERNATE_ROUTING_DESIGNATOR,COMPLETION_SUBINVENTORY,COMPLETION_LOCATOR_ID,SUB_LOCATOR_CONTROL,DEMAND_CLASS,SCHEDULE_GROUP_NAME,SCHEDULE_GROUP_ID,BUILD_SEQUENCE,LINE_CODE,LINE_ID,PROJECT_NAME,PROJECT_NUMBER,PROJECT_ID,TASK_NAME,TASK_NUMBER,TASK_ID,END_ITEM_UNIT_NUMBER,ATTRIBUTE_CATEGORY,ATTRIBUTE1,ATTRIBUTE2,ATTRIBUTE3,ATTRIBUTE4,ATTRIBUTE5,ATTRIBUTE6,ATTRIBUTE7,ATTRIBUTE8,ATTRIBUTE9,ATTRIBUTE10,ATTRIBUTE11,ATTRIBUTE12,ATTRIBUTE13,ATTRIBUTE14,ATTRIBUTE15,STATUS_TYPE_DISP,WIP_SUPPLY_TYPE_DISP,OVERCOMPLETION_TOLERANCE_TYPE,OVERCOMPLETION_TOLERANCE_VALUE,KANBAN_CARD_ID,KANBAN_CARD_NUMBER,PO_CREATION_TIME,PRIORITY,DUE_DATE,EST_SCRAP_ACCOUNT,EST_SCRAP_VAR_ACCOUNT,ENTITY_TYPE,DUE_DATE_PENALTY,DUE_DATE_TOLERANCE,COPRODUCTS_SUPPLY,REQUESTED_START_DATE,SERIALIZATION_START_OP,ACTUAL_START_DATE,EXPECTED_HOLD_RELEASE_DATE --hive-overwrite --m 1
        sqoop_command = f"""
        sqoop import \
        --connect {jdbc_url} \
        --username {username} \
        --password {password} \
        --table {source_table} \
        --hive-import \
        --hive-database bi_ods \
        --hive-table {sink_table} \
        --delete-target-dir \
        --hive-drop-import-delims \
        --fields-terminated-by '\\001' \
        --lines-terminated-by '\\n' \
        --null-string '\\\\N' \
        --null-non-string '\\\\N' \
        --map-column-java {sqoop_param}  \
        --map-column-hive {sqoop_param}   \
        --hive-overwrite \
        --m 1
        """
        logger.info("依据字段的COL抽数(指定列抽数),SQOOP执行命令:{}".format(sqoop_command))
        os.system(sqoop_command)
    elif sqoop_type == "QUERY":
        # sqoop import --connect jdbc:oracle:thin:@ebsdb-scan.kinwong.com:1531/prod --username hadoop --password vSWnGLcdd8ch --table APPS.WIP_DISCRETE_JOBS_V --hive-import --hive-database bi_ods --hive-table ODS_APPS_WIP_DISCRETE_JOBS_V --delete-target-dir --hive-drop-import-delims --fields-terminated-by '\001' --lines-terminated-by '\n' --null-string '\\N' --null-non-string '\\N' --columns WIP_ENTITY_ID,WIP_ENTITY_NAME,ORGANIZATION_ID,LAST_UPDATE_DATE,LAST_UPDATED_BY,CREATION_DATE,CREATED_BY,LAST_UPDATE_LOGIN,REQUEST_ID,PROGRAM_APPLICATION_ID,PROGRAM_ID,PROGRAM_UPDATE_DATE,DESCRIPTION,STATUS_TYPE,PRIMARY_ITEM_ID,FIRM_PLANNED_FLAG,JOB_TYPE,JOB_TYPE_MEANING,WIP_SUPPLY_TYPE,CLASS_CODE,MATERIAL_ACCOUNT,MATERIAL_OVERHEAD_ACCOUNT,RESOURCE_ACCOUNT,OUTSIDE_PROCESSING_ACCOUNT,MATERIAL_VARIANCE_ACCOUNT,RESOURCE_VARIANCE_ACCOUNT,OUTSIDE_PROC_VARIANCE_ACCOUNT,STD_COST_ADJUSTMENT_ACCOUNT,OVERHEAD_ACCOUNT,OVERHEAD_VARIANCE_ACCOUNT,SCHEDULED_START_DATE,DATE_RELEASED,SCHEDULED_COMPLETION_DATE,DATE_COMPLETED,DATE_CLOSED,START_QUANTITY,QUANTITY_REMAINING,QUANTITY_COMPLETED,QUANTITY_SCRAPPED,NET_QUANTITY,BOM_REFERENCE_ID,ROUTING_REFERENCE_ID,COMMON_BOM_SEQUENCE_ID,COMMON_ROUTING_SEQUENCE_ID,BOM_REVISION,ROUTING_REVISION,BOM_REVISION_DATE,ROUTING_REVISION_DATE,LOT_NUMBER,ALTERNATE_BOM_DESIGNATOR,ALTERNATE_ROUTING_DESIGNATOR,COMPLETION_SUBINVENTORY,COMPLETION_LOCATOR_ID,SUB_LOCATOR_CONTROL,DEMAND_CLASS,SCHEDULE_GROUP_NAME,SCHEDULE_GROUP_ID,BUILD_SEQUENCE,LINE_CODE,LINE_ID,PROJECT_NAME,PROJECT_NUMBER,PROJECT_ID,TASK_NAME,TASK_NUMBER,TASK_ID,END_ITEM_UNIT_NUMBER,ATTRIBUTE_CATEGORY,ATTRIBUTE1,ATTRIBUTE2,ATTRIBUTE3,ATTRIBUTE4,ATTRIBUTE5,ATTRIBUTE6,ATTRIBUTE7,ATTRIBUTE8,ATTRIBUTE9,ATTRIBUTE10,ATTRIBUTE11,ATTRIBUTE12,ATTRIBUTE13,ATTRIBUTE14,ATTRIBUTE15,STATUS_TYPE_DISP,WIP_SUPPLY_TYPE_DISP,OVERCOMPLETION_TOLERANCE_TYPE,OVERCOMPLETION_TOLERANCE_VALUE,KANBAN_CARD_ID,KANBAN_CARD_NUMBER,PO_CREATION_TIME,PRIORITY,DUE_DATE,EST_SCRAP_ACCOUNT,EST_SCRAP_VAR_ACCOUNT,ENTITY_TYPE,DUE_DATE_PENALTY,DUE_DATE_TOLERANCE,COPRODUCTS_SUPPLY,REQUESTED_START_DATE,SERIALIZATION_START_OP,ACTUAL_START_DATE,EXPECTED_HOLD_RELEASE_DATE --hive-overwrite --m 1
        sqoop_command = f"""
        sqoop import \
        --connect {jdbc_url} \
        --username {username} \
        --password {password} \
        --target-dir /sqoop/conditiontest/{sink_table} \
        --delete-target-dir \
        --query "{sqoop_param}   and \\$CONDITIONS " \
        --hive-import \
        --hive-database bi_ods \
        --hive-table {sink_table} \
        --hive-drop-import-delims \
        --fields-terminated-by '\\001' \
        --lines-terminated-by '\\n' \
        --null-string '\\\\N' \
        --null-non-string '\\\\N' \
        --hive-overwrite \
        --m 1
        """
        logger.info("自定义sql抽数,SQOOP执行命令:{}".format(sqoop_command))
        os.system(sqoop_command)
    else:
        logger.info("未知类型sqoop抽数,请检查!")

def execute_distribute_sqoop_command(jdbc_url,
                                     username,
                                     source_table,
                                     sink_table,
                                     password,
                                     sqoop_type,sqoop_param, parallelism):
    """
    执行sqoop命令
    :param sqoop_command:
    :param sqoop_type: 同步类型:{SRM、NORMAL、ROWID、INCRE、COL、QUERY}
    :param parallelism: 任务并行度
    :return:
    """
    logger.info("执行sqoop命令...!")
    if sqoop_type == "NORMAL":
        logger.info("NORMAL抽数")
        sqoop_command = f"""

        """
        os.system(sqoop_command)
    elif sqoop_type == "ROWID":
        logger.info("ROWID抽数")
        sqoop_command = f"""
        
        """
        os.system(sqoop_command)
    elif sqoop_type == "INCRE":
        logger.info("INCRE抽数")
        sqoop_command = f"""
        
        """
        os.system(sqoop_command)
    elif sqoop_type == "COL":
        logger.info("COL抽数")
        sqoop_command = f"""
        
        """
        os.system(sqoop_command)
    elif sqoop_type == "QUERY":
        logger.info("QUERY抽数")
        sqoop_command = f"""
        
        """
        os.system(sqoop_command)
    else:
        logger.info("未知类型sqoop抽数,请检查!")




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
    jdbc_url = "jdbc:oracle:thin:@ebsdb-scan.kinwong.com:1531/prod"
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
    if pipeline_type == 'oracle_sync_impala':
        oracle_sync_impala(jdbc_url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    # elif pipeline_type == 'mysql_sync_impala':
    #     mysql_sync_impala(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    # elif pipeline_type == 'postgresql_sync_impala':
    #     postgresql_sync_impala(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    # elif pipeline_type == 'impala_sync_mysql':
    #     impala_sync_mysql(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    # elif pipeline_type == 'impala_sync_oracle':
    #     impala_sync_oracle(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    # elif pipeline_type == 'impala_sync_postgresql':
    #     impala_sync_postgresql(url,username,password,source_table,sink_table,sqoop_type,is_distributed,split_by,parallelism)
    else:
        logger.info("未知类型数据同步,请检查!")

    # data = json.loads(json_str)
    # # 获取姓名和年龄
    # name = data['name']
    # age = data['age']
    # print(name)

    print(" >>> sqoop抽数结束!")