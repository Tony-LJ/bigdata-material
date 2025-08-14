#!/bin/bash
# ################################
#
# */5 * * * * /bin/bash /opt/kw_bigdata_monitor.sh >> /var/log/kw_bigdata_monitor.log 2>&1
# ################################
# 企业微信 API 信息（请替换成你的）
CORP_ID="your_corp_id"      # 企业 ID
SECRET="your_secret"        # 应用 Secret
AGENT_ID="your_agent_id"    # 应用 ID
USER="luojie|jinyue|chenliu|zengyu"             # 接收告警的用户名（可以是多个用户，用 '|' 分隔）
log_timestamp=$(date "+%Y-%m-%d %H:%M:%S")

# 获取 AccessToken
get_access_token() {
    response=$(curl -s -G "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CORP_ID&corpsecret=$SECRET")
    echo "$response" | jq -r .access_token
}

# 发送企业微信告警
send_alert() {
    local message="⚠️ [告警] 服务器 $SERVER_IP 端口 $SERVER_PORT 不可用！请检查！"
    local token=$(get_access_token)

    curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$token" \
        -H "Content-Type: application/json" \
        -d "{
            \"touser\": \"$USER\",
            \"msgtype\": \"text\",
            \"agentid\": $AGENT_ID,
            \"text\": { \"content\": \"$message\" }
        }"
}

send_qiyeweixin_alert() {
  content=$1
  content=${content//\ /}
  content=${content//\"/}
  date=$(date +%Y-%m-%d)
  time=$(date "+%H:%M:%S")
  content="
  **数据集群组件运行状态检查[new]**
      >检查日期：<font color='blue'>$date $time</font>
      >巡检人员：<font color='black'>大数据团队</font>
      >告警内容：<font  color='warning'>$content</font>
  "
  webHookUrl="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=80e05c6d-310b-4fc7-a9c5-966b0bea99be"
  content='{"msgtype": "markdown","markdown": {"content": "'$content'","mentioned_list":"@all"},}'
  echo "content : $content"
  curl --data-ascii "$content" $webHookUrl
  echo "over!"
}

# 检测 hadoop HDFS NameNode服务是否正常
check_hdfs_namenode_status() {
  echo "-------------------------------------------------------"
  echo "hadoop HDFS - NameNode ："
  for ip in 10.53.0.71 10.53.0.72
  do
      ssh root@$ip "ps -fe|grep NameNode |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "HDFS-NameNode运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检测 hadoop HDFS DataNode服务是否正常
check_hdfs_datanode_status() {
  echo "-------------------------------------------------------"
  echo "hadoop HDFS - DataNode ："
  for ip in 10.53.0.71 10.53.0.72 10.53.0.73 10.53.0.74 10.53.0.75
  do
      ssh root@$ip "ps -fe|grep DataNode |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "HDFS-DataNode运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检查hadoop YARN ResourceManager服务是否正常
check_yarn_rm_status() {
  echo "-------------------------------------------------------"
  echo "hadoop YARN - ResourceManager ："
  for ip in 10.53.0.71
  do
      ssh root@$ip "ps -fe|grep ResourceManager |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "YARN-ResourceManager运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检查hadoop YARN NodeManager服务是否正常
check_yarn_nm_status() {
  echo "-------------------------------------------------------"
  echo "hadoop YARN - NodeManager ："
  for ip in 10.53.0.71 10.53.0.72 10.53.0.73 10.53.0.74 10.53.0.75
  do
      ssh root@$ip "ps -fe|grep NodeManager |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "YARN-NodeManager运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检查impala-server服务是否正常
check_impala_server_status() {
  # 检测 impala-server
  echo "-------------------------------------------------------"
  echo "impala - impala-server ："
  for ip in 10.53.0.71 10.53.0.72 10.53.0.73 10.53.0.74 10.53.0.75
  do
      ssh root@$ip "ps -fe|grep impala |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "impala-server运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检查HiveMetaStore服务是否正常
check_hivemetastore_status() {
  # 检测 impala-server
  echo "-------------------------------------------------------"
  echo "hive - HiveMetaStore  ："
  for ip in 10.53.0.71 10.53.0.72 10.53.0.73
  do
      ssh root@$ip "ps -fe|grep HiveMetaStore  |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "HiveMetaStore运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检查HiveServer2 服务是否正常
check_hiveserver2_status() {
  # 检测 impala-server
  echo "-------------------------------------------------------"
  echo "hive - HiveServer2  ："
  for ip in 10.53.0.71 10.53.0.72 10.53.0.73
  do
      ssh root@$ip "ps -fe|grep HiveServer2  |grep -v grep >/dev/null 2>&1"
      if [ $? -ne 0 ]
      then
          echo -e "$ip： [\033[31m未启动\033[0m]"
          send_qiyeweixin_alert "HiveServer2运行异常,IP地址:"$ip
      else
          echo -e "$ip： [\033[32m正常\033[0m]"
      fi
  done
}

# 检查服务器磁盘
check_disk_status(){
    echo "-------------------------------------------------------"
    echo "Lunix- Disk:"
    IP_LIST=("10.53.0.71" "10.53.0.72" "10.53.0.73" "10.53.0.74" "10.53.0.75")
    # 定义磁盘使用率的阈值（例如：80%为80）
    THRESHOLD=80
    for ip in "${IP_LIST[@]}"; do
        # 获取磁盘使用率
        DISK_USAGE=$(ssh root@"$ip" df /data | grep / | awk '{print $5}' | cut -d'%' -f1)
        # 判断磁盘使用率是否超过阈值
        if [ "$DISK_USAGE" -gt "$THRESHOLD" ]; then
            echo "Disk usage on $ip is above the threshold ($DISK_USAGE% > $THRESHOLD%)"
            send_qiyeweixin_alert "⚠️磁盘使用率$DISK_USAGE,超过阈值$THRESHOLD，请检查,IP地址:"$ip
        else
            echo "Disk usage on $ip is within the threshold ($DISK_USAGE% <= $THRESHOLD%)"
        fi
    done
}

check_memory_status(){
    echo "-------------------------------------------------------"
    echo "Lunix- Memory:"
    IP_LIST=("10.53.0.71" "10.53.0.72" "10.53.0.73" "10.53.0.74" "10.53.0.75")
    # 定义内存使用率的阈值（例如：80%为80）
    THRESHOLD=80
    for ip in "${IP_LIST[@]}"; do
        # 获取内存使用率
        MEMORY_USAGE=$(ssh root@$ip free | grep Mem | awk '{print $3/$2 * 100.0}')
        # 判断磁盘使用率是否超过阈值
      if (( $(echo "$MEMORY_USAGE > $THRESHOLD" | bc -l) )); then
            echo "Memory usage on $ip is above the threshold ($MEMORY_USAGE% > $THRESHOLD%)"
            send_qiyeweixin_alert "⚠️内存使用率$MEMORY_USAGE%,超过阈值$THRESHOLD%，请检查,IP地址:"$ip
        else
            echo "Memory usage on $ip is within the threshold ($MEMORY_USAGE% <= $THRESHOLD%)"
        fi
    done
}

check_cpu_status(){
    echo "-------------------------------------------------------"
    echo "Lunix- CPU:"
    IP_LIST=("10.53.0.71" "10.53.0.72" "10.53.0.73" "10.53.0.74" "10.53.0.75")
    # 定义磁盘使用率的阈值（例如：80%为80）
    THRESHOLD=90
    for ip in "${IP_LIST[@]}"; do
        # 获取磁盘使用率
        CPU_USAGE=$(ssh root@$ip top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
        # 判断磁盘使用率是否超过阈值
        if (( $(echo "$CPU_USAGE > $THRESHOLD" | bc -l) )); then
            echo "CPU usage on $ip is above the threshold ($CPU_USAGE% > $THRESHOLD%)"
            send_qiyeweixin_alert "⚠️CPU使用率$CPU_USAGE%,超过阈值$THRESHOLD%，请检查,IP地址:"$ip
        else
            echo "CPU usage on $ip is within the threshold ($CPU_USAGE% <= $THRESHOLD%)"
        fi
    done
}

printf "\n[%s] ===== Script Execution Start =====\n" "$log_timestamp"
# ##### 服务检查硬盘、内存、CPU使用情况检查
check_disk_status
check_memory_status
check_cpu_status
# ##### 数据集群组件检查
# Hadoop检查
check_hdfs_namenode_status
check_hdfs_datanode_status
check_yarn_rm_status
check_yarn_nm_status
# Hive检查
check_hiveserver2_status
check_hivemetastore_status
# Impala检查
check_impala_server_status
# Airflow检查
printf "\n[%s] ===== Script Execution End =====\n" "$log_timestamp"
#find /opt/log -type f -name "kw_bigdata_monitor.*.log" -mtime +7 -exec rm {} \;

