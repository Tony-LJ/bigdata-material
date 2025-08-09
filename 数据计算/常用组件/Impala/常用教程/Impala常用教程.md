
# Impala常用教程

---

## 常用命令
```.text
1.删除指定分区数据
alter table bi_data.dwd_lcsmt_oms_pdm_yield_record_to_hadoop_di drop if exists partition(pt_d='2025-08-08');
```