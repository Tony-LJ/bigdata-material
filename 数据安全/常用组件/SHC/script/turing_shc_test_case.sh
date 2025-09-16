#!/bin/bash
# #################################################
# descr: 基于SHC加密SHELL脚本，设置加密文件的过期时间,并指定到期消息提示内容
# shc -e 15/09/2025 -m "The script has expired, please contact CoCo" -v -f /opt/script/turing_shc_test_case.sh
# author: Tony
# date: 2025-09-20
# #################################################
for i in `seq 1 9` #外层打印
do
  for j in `seq 1 $i` #内层打印
  do
    echo -ne "$j*$i=$[$j*$i]\t"
  done
    echo ""
done

##注释
# $连着[] = 表示算术运算
# -n = 不换行
# -s = 处理特殊符号
# \t = 横制表符