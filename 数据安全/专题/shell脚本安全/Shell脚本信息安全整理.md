
# Shell脚本信息安全整理

---

## Shell脚本加密
### 基于SHC实现
- [shc环境安装]()
```.text
方式1：包管理器安装（推荐）
# Ubuntu/Debian
sudo apt install shc
# CentOS/RHEL
sudo yum install epel-release && sudo yum install shc
方式2：
wget http://www.datsi.fi.upm.es/~frosal/sources/shc-3.8.9.tgz
tar xvfz shc-3.8.9.tgz && cd shc-3.8.9
make && sudo make install
```
- [shc使用]()
```.text
1.加密脚本
基础命令格式：
shc -f your_script.sh  # 生成 your_script.sh.x（二进制）和 your_script.sh.x.c（C源码）
常用参数：
-r：放宽安全限制，允许跨系统运行（解决环境兼容性问题）。
-e DD/MM/YYYY：设置过期时间，超时拒绝执行。
-m "message"：自定义过期提示信息。
示例：
shc -v -r -f your_script.sh -o encrypted_script
运行加密后的脚本：
./your_script.sh.x  # 直接执行二进制文件
```

## 常规加密的陷阱：脚本执行卡死

























## 参考资料
- [Shell脚本加密操作：让用户可执行，不可查看脚本源码 —— shc 实战避坑指南](https://blog.csdn.net/weixin_41004518/article/details/149541794)