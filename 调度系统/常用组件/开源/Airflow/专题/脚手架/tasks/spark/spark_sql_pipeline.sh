#!/bin/bash
# #################################################
# descr: spark-sql通用计算pipeline
# author: Tony
# date: 2025-09-20
# #################################################
export LC_ALL=zh_CN.utf8
# 测试阶段日更，线上保持周更即可
DATA_DATE=$1

# 输入参数校验
if [[ ${DATA_DATE} -eq "" ]]; then
  DATA_DATE=$(date "+%Y%m%d")
fi
BIZ_DATE=`date +%Y%m%d -d "${DATA_DATE} -1 day"`

spark-sql --master yarn --deploy-mode client -e"
insert overwrite table bi_ods.ods_mdmuser_mdm_model_ext
select * from bi_sync.ods_mdmuser_mdm_model_ext
"

if [[ $? -eq 0 ]]; then
	echo ">>>数据同步结束，同步日期:${BIZ_DATE}"
else
	exit 1
fi