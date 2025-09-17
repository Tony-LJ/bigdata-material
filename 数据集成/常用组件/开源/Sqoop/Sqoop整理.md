
# Sqoop整理

---

## Sqoop抽数
```.text
sqoop import \
--connect jdbc:oracle:thin:@ebsdb-scan.kinwong.com:1531/prod \
--username hadoop \
--password vSWnGLcdd8ch \
--table ONT.OE_ORDER_LINES_ALL \
--hive-import \
--hive-database bi_ods \
--hive-table ODS_OE_ORDER_LINES_ALL \
--delete-target-dir \
--hive-drop-import-delims \
--fields-terminated-by '\001' \
--lines-terminated-by '\n' \
--null-string '\\N' \
--null-non-string '\\N' \
--hive-overwrite \
--split-by org_id \
--m 5
```



## 参考资料
- [sqoop --split-by详解](https://blog.csdn.net/jsjsjs1789/article/details/70093104)