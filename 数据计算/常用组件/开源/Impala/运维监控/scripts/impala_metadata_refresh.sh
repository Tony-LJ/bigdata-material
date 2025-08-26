#!/bin/bash
##############################
# */1 * * * * sshpass -p 'EEEeee111' ssh root@10.53.0.1 sh /srv/tmp/impala_metadata_refresh.sh
##############################
# 设置Impala的连接属性
im_host="10.53.0.71"
im_port="21050"
im_user="impala"
im_password=""

# 刷新元数据
echo "刷新Impala元数据..."
# 执行刷新元数据的Impala命令
cmd="INVALIDATE METADATA;"
result=$(echo "$cmd" | beeline -u  "jdbc:hive2//$im_host:$im_port" -n $im_user -p $im_password)
echo "刷新结果: $result"
echo "刷新完成！"


