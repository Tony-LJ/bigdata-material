#!/bin/bash
# #################################################
# descr: openssl enc命令加密文件
# author: Tony
# date: 2025-09-20
# #################################################
# 设置变量
input_file="/opt/script/example.txt"
output_file="/opt/script/encrypted_example.txt"
password="Turing@123456789"
cipher="aes-256-cbc"  # 加密算法
# 加密文件
openssl enc -aes-256-cbc -salt -in "$input_file" -out "$output_file" -pass pass:"$password"