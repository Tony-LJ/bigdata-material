
# Impala常用教程

---

## 常用命令
```.text
1.删除指定分区数据
alter table bi_data.dwd_lcsmt_oms_pdm_yield_record_to_hadoop_di drop if exists partition(pt_d='2025-08-08');
```


## 常用函数
### 日期函数
```.text
select stampdatetime
      ,to_date(t.stampdatetime)
      ,to_date(trunc(years_sub(now(),1),'yyyy'))
from bi_data.dwd_cux_cux_lotnumtoebs_t  as t
where to_date(t.stampdatetime) > to_date(date_sub(now(),2)) and to_date(t.stampdatetime) <= to_date(date_sub(now(),1))
-- 获取8-11之前的数据,即T-1之前的数据
-- and to_date(t.stampdatetime) <= to_date(date_sub(now(),2))
-- 获取8-11的数据,即T-1当天的数据
-- and to_date(t.stampdatetime) > to_date(date_sub(now(),2)) and to_date(t.stampdatetime) <= to_date(date_sub(now(),1))
-- 获取8-12的数据,即T当天的数据
-- and to_date(t.stampdatetime) > to_date(date_sub(now(),1)) and to_date(t.stampdatetime) <= to_date(date_sub(now(),0))

select to_date(date_sub(now(),2)); 

– 取当天
select cast(now() as timestamp)
select from_unixtime(unix_timestamp(),‘yyyyMMdd’) a

– 取当月
select from_unixtime(unix_timestamp(),‘yyyyMM’)
select from_unixtime(unix_timestamp(),‘yyyy-MM’)
select substr(cast(now() as string) , 1,7)
- 取上月
select substr(cast(to_date(date_add(date_trunc('month',to_date(date_sub(now(),1))),-1)) as string) , 1,7);

– 取当年
select from_unixtime(unix_timestamp(),‘yyyy’)
select substr(cast(now() as string) , 1,4)
- 取去年
select to_date(trunc(years_sub(now(),1),'yyyy'));

– 取昨天
select date_sub(now(),interval 1 day )

– 现在日期加1天
select days_add(now(),1) a
select date_add(now(),interval 1 day) aa

– 现在日期相减1天
select date_sub(now(), interval 1 days)
select date_sub(now(), interval 1 day)

– 日期相差天数
select datediff(‘2018-08-05’,‘2018-08-03’) a
select datediff(‘2018-12-07 00:00:00.0’,‘2019-06-04 00:00:00.0’) a —179天
select abs( cast( ((unix_timestamp(‘2018-12-07 00:00:00.0’)-unix_timestamp(‘2019-06-04 00:00:00.0’))/86400) as double) ) a

select abs(cast(substr(‘2019-04-05 00:00:00.0’,9,2)as double)- cast(substr(‘2019-04-01 00:00:00.0’,9,2) as double)) a

– 数据四舍五入保留2位小数
select cast(cast(round(166/34148,2) as decimal(20,2)) as string)

- 年月日期截取
select substr(cast(to_date(stampdatetime) as string) , 1,7)  from bi_data.dwd_cux_cux_lotnumtoebs_t;
```
- [行转列 group_concat(字段名,‘；’)]()
```.text
– 行转列 group_concat(字段名,‘；’)
select cons_no,group_concat(tg_id,‘；’) 台区编号
from 表名
group by cons_no
```