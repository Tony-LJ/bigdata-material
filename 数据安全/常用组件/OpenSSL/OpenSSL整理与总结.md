
# OpenSSL整理与总结

---

## OpenSSL介绍
```.text
OpenSSL 库提供了一套全面的密码功能，包括数字签名、对称和非对称加密、散列和证书管理。它还支持范围广泛的密码算法，包括 RSA、DSA、Diffie-Hellman 和椭圆曲线密码术。
```

## 安装部署
```.text
安装构建 OpenSSL 所需的依赖项
sudo yum -y groupinstall "Development Tools"
下载 OpenSSL 1.1.x 的源代码，其中x替换为所需的实际版本
mkdir -p /opt/module
wget https://www.openssl.org/source/openssl-1.1.1t.tar.gz --no-check-certificate
tar xvf openssl-1.1.1t.tar.gz
cd openssl-1.1*/

配置 OpenSSL:
./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl

使用make命令构建 OpenSSL 1.1.x
sudo make install
在 CentOS 7 / RHEL 7 上安装 OpenSSL 1.1.1
sudo make install
更新共享库缓存
sudo ldconfig

更新系统范围的 OpenSSL 配置：
sudo tee /etc/profile.d/openssl.sh<<EOF
export PATH=/usr/local/openssl/bin:\$PATH
export LD_LIBRARY_PATH=/usr/local/openssl/lib:\$LD_LIBRARY_PATH
EOF

重新加载shell环境：
source /etc/profile.d/openssl.sh

重新登录并验证CentOS 7/RHEL 7上是否安装了OpenSSL 1.1.1
> 查看位置
which openssl
/usr/local/openssl/bin/openssl
> 查看版本openssl version
OpenSSL 1.1.1t  7 Feb 2023
```

## 使用教程
```.text

```



## openssl aes-256-cbc命令常用场景
- [加密/解密文件或数据]()
```.text
用于保护敏感数据，如配置文件、数据库备份、通信内容等。
支持对称加密，确保只有持有密钥的双方可以解密数据。
```
- [数据传输安全]()
```.text
在数据传输过程中，使用 AES-256-CBC 加密保证数据机密性。
常用于安全通信协议（如 HTTPS、SSH）之外的场景。
```
- [自动化脚本中的加密操作]()
```.text
在 CI/CD 管道或自动化脚本中，用于加密/解密敏感信息（如凭据、密钥）。
兼容性需求
```









## 参考资料
- [对shell脚本敏感命令进行加密执行](https://blog.csdn.net/unbuntu_luo/article/details/146467541)
- [如何在CentOS 7/RHEL 7上安装OpenSSL 1.1.x](https://blog.csdn.net/frenzytechai/article/details/131264516)











