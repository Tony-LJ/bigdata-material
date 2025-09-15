#!/bin/bash
# #################################################
# descr: impala-sql通用计算pipeline
# author: Tony
# date: 2025-09-20
# #################################################

ssh root@10.53.0.1 "nohup impala-shell -f /root/bi/bi_data/bi_data_dwd_cux_cux_lotnumtoebs_t.sql ; "
