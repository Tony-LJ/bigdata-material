#!/bin/bash
# #################################################
# descr: impala-sql通用计算pipeline
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

ssh root@10.53.0.1 "nohup impala-shell -f /root/bi/bi_data/bi_data_dwd_cux_cux_lotnumtoebs_t.sql ; "
