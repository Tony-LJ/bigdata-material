#!/bin/bash
# #################################################
# descr: 加密这条命令：cat /opt/script/setjavahome.sh 如何利用openssl aes-256-cbc 实现加密和解密，并执行命令
# author: Tony
# date: 2025-09-20
# #################################################
# 生成密钥和 IV（32 字节密钥，16 字节 IV）
KEY=$(openssl rand -hex 32)
IV=$(openssl rand -hex 16)

# 加密命令
ENCRYPTED_COMMAND=$(echo "cat /opt/script/setjavahome.sh" | openssl aes-256-cbc -K ${KEY} -iv ${IV} -base64)

# 输出加密结果
echo "Key: ${KEY}"
echo "IV: ${IV}"
echo "Encrypted Command: ${ENCRYPTED_COMMAND}"

# 解密并执行
DECRYPTED_COMMAND=$(echo "${ENCRYPTED_COMMAND}" | openssl aes-256-cbc -K ${KEY} -iv ${IV} -base64 -d)
eval ${DECRYPTED_COMMAND}