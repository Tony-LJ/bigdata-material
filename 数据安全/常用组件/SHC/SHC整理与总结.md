
# SHC整理与总结

---

## SHC介绍
```.text
Shc可以用来对shell脚本进行加密，可以将shell脚本转换为一个可执行的二进制文件。经过shc对shell脚本进行加密后，会同时生成两种个新的文件，一个是加密后的可执行的二进制文件（文件名以.x结束），另一个是C语言的原文件（文件名以.x.c结束）
```

## 安装部署
```.text
shc依赖gcc，需要先安装gcc：
yum -y install gcc shc
```

## 使用教程
- [Usage]()
```.text
shc Usage: shc [-e date] [-m addr] [-i iopt] [-x cmnd] [-l lopt] [-rvDTCAh] -f script
    -e %s  Expiration date in dd/mm/yyyy format [none] #设置过期时间
    -m %s  Message to display upon expiration ["Please contact your provider"] #过期信息提示
    -f %s  File name of the script to compile #加密脚本名称
    -i %s  Inline option for the shell interpreter i.e: -e
    -x %s  eXec command, as a printf format i.e: exec('%s',@ARGV);
    -l %s  Last shell option i.e: --
    -r     Relax security. Make a redistributable binary #在系统通用
    -v     Verbose compilation #详细汇编
    -D     Switch ON debug exec calls [OFF]
    -T     Allow binary to be traceable [no]
    -C     Display license and exit #显示许可证并退出
    -A     Display abstract and exit #显示摘要和退出
    -h     Display help and exit #显示帮助和退出
```
- [简单使用]()
```.text
使用加密命令:
shc -v -f /opt/script/turing_shc_test_case.sh
生成:
shc shll=sh
shc [-i]=-c
shc [-x]=exec '%s' "$@"
shc [-l]=
shc opts=
shc: cc   turing_shc_test_case.sh.x.c -o turing_shc_test_case.sh.x
shc: strip turing_shc_test_case.sh.x
shc: chmod ug=rwx,o=rx turing_shc_test_case.sh.x
说明：
turing_shc_test_case.sh 是原始的未加密脚本
turing_shc_test_case.sh.x 是二进制格式的加密shell脚本
turing_shc_test_case.sh.x.c 是turing_test_case.sh 文件的C源代码

使用file命令查看文件的类型
file turing_shc_test_case.sh.x

验证加密后的脚本是否可正常执行
sh /opt/script/turing_shc_test_case.sh.x.c

设置Shell脚本的过期时间,并指定自定义的到期消息提示内容
shc -e 24/09/2021 -m "The script has expired, please contact CoCo" -v -f /opt/script/turing_shc_test_case.sh
```

- [shell脚本文件通过shc工具加密，生成静态链接可执行文件]()
```.text


```
- [shell脚本文件通过shc工具加密，生成二机制可执行文件]()
```.text

```










## 参考资料
- [Linux centos7安装shc加密shell脚本命令行工具](https://blog.51cto.com/zhangxueliang/11709061)










