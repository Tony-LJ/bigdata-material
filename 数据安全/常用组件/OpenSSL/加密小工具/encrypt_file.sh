#!/bin/bash
# #################################################
# descr: openssl解密小工具
# usage: ./encrypt_file.sh your_input_file.txt encrypted_output_file.txt your_password
# author: Tony
# date: 2025-09-20
# #################################################
# 使用OpenSSL加密文件
# 参数1: 要加密的文件路径
# 参数2: 输出文件的路径
# 参数3: 密码（用于加密）

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file> <output_file> <password>"
    exit 1
fi

openssl enc -aes-256-cbc -salt -in "$1" -out "$2" -pass pass:"$3"

echo "File encrypted successfully."
