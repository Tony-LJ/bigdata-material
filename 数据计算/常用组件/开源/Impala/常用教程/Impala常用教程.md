
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
select to_date(trunc(months_sub(date_sub(now(),1),1),'mm'));

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

----------------------------------------------------------------------------------------------------------
1.时间戳转格式化为日期(String)
select from_unixtime(unix_timestamp(), 'yyyy-MM-dd HH:mm:ss');
select from_unixtime(1755302400, 'yyyy-MM-dd HH:mm:ss');
select from_unixtime(1755067761, 'yyyy-MM-dd HH:mm:ss');
select from_unixtime(unix_timestamp() + 60*60*24*30, 'yyyy-MM-dd')  -- 时间戳加30天
select from_unixtime(unix_timestamp() - 60*60*24*30, 'yyyy-MM-dd')  -- 时间戳减30天
select unix_timestamp(now() + interval 3 days)    -- 时间戳加3天
2.获取当前时间戳
unix_timestamp()
3.时间戳取整
select date_trunc('year',now())
select date_trunc('month',now())
select date_trunc('week',now())
select date_trunc('day',now())
select date_trunc('hour',now())
select date_trunc('minute',now())
4.日期格式化
select from_unixtime(unix_timestamp('2021-11-12 11:12:11'),'yyyy-MM-dd HH:mm:ss')
5.精确计算指定天的起止时间
5.1 前一天的起止时间
select date_add(date_trunc('day', now()), interval -1 days);
select date_add(date_trunc('day', now()), interval -0 days) + interval -1 second 
select from_unixtime(unix_timestamp(date_add(date_trunc('day', now()), interval -1 days)),'yyyy-MM-dd HH:mm:ss')  -- 2025-08-12 00:00:00
select from_unixtime(unix_timestamp(date_add(date_trunc('day', now()), interval -0 days) + interval -1 second),'yyyy-MM-dd HH:mm:ss')   -- 2025-08-12 23:59:59
5.2 上个月的起止时间
select unix_timestamp(trunc(add_months(now(), -1), 'mm')) as first_day_of_last_month;                 -- 2025-07-01 00:00:00
select unix_timestamp(last_day(add_months(now(), -1))) + ((60*60*24)*1)-1 as last_day_of_last_month;  -- 2025-07-31 23:59:59
5.2 去年的起止时间
select  as first_day_of_last_year;                 -- 2025-07-01 00:00:00
select  as last_day_of_last_year;  -- 2025-07-31 23:59:59
6.获取指定天内的数据
select * 
from bi_ods.ods_mtl_transaction_lot_numbers
where to_date(transaction_date) = '2025-08-12'
```
- [截断函数]()
```.text
TRUNC函数用于对值进行截断。
用法有两种：TRUNC（NUMBER）表示截断数字，TRUNC（date）表示截断日期。
select trunc(15.79,1)  -- 15.7
select trunc(156.79,-1)  -- 150
```

- [行转列 group_concat(字段名,‘；’)]()
```.text
– 行转列 group_concat(字段名,‘；’)
select cons_no,group_concat(tg_id,‘；’) 台区编号
from 表名
group by cons_no
```

- [小技巧]()
```.text
create table bi_data.dwd_cux_cux_lotnumtoebs_t_bak20250813 like bi_data.dwd_cux_cux_lotnumtoebs_t ; -- 创建备份数据表
insert overwrite table bi_data.dwd_cux_cux_lotnumtoebs_t_bak20250813
select * from bi_data.dwd_cux_cux_lotnumtoebs_t;  -- 数据写入备份表
insert overwrite table bi_data.dwd_cux_cux_lotnumtoebs_t partition (pt_m)
select *,to_date(trunc(stampdatetime,'MM')) as pt_m from bi_data.dwd_cux_cux_lotnumtoebs_t_bak20250813; -- 备份表重新回写新分区表
```

- [按照日期字段分区写入]()
```.text
insert overwrite table  bi_data.dwd_cux_cux_lotnumtoebs_t  
PARTITION (pt_m)
select
coalesce(cast(lotnumtoebs_id as string)  ,'-1')            as lotnumtoebs_id      -- id
,coalesce(stampdatetime             ,'-1')                  as stampdatetime       -- 过数时间
,coalesce(item_code                   ,'-1')                  as item_code           -- 物料编码
,coalesce(cust_code                 ,'-1')                  as cust_code           --  '客户编码'
,coalesce(order_number              ,'-1')                  as order_number        --  '订单编号'
,coalesce(wip_entity_num            ,'-1')                  as wip_entity_num      --  '工单号'
,coalesce(frm_proc                  ,'-1')                  as frm_proc            -- 前工序代码
,coalesce(item_version                ,'-1')                  as item_version        -- 大版本号
,coalesce(pdversion                 ,'-1')                  as pdversion           -- 内部版本号
,coalesce(layup_num                 ,'-1')                  as layup_num           -- 小版本号
,coalesce(lotno                     ,'-1')                  as lotno               -- lot卡号
,coalesce(suffix                    ,'-1')                  as suffix              -- 当前层数编码
,coalesce(frm_proc_name             ,'-1')                  as frm_proc_name       -- 前工序名称
,coalesce(cast(trans_qty as decimal(38,10)) ,0)             as trans_qty           -- 过数数量
,coalesce(cast(milayerid as string)       ,'-1')            as milayerid           -- mi层id
,coalesce(cuflag                    ,'-1')                  as cuflag              -- 是否cu
,coalesce(to_proc                   ,'-1')                  as to_proc             -- 后工序代码
,coalesce(frm_seq                   ,'-1')                  as frm_seq             -- 前工序序号
,coalesce(to_seq                    ,'-1')                  as to_seq              -- 后工序序号
,coalesce(transtype_name            ,'-1')                  as transtype_name      -- 过数类型
,coalesce(nexsuffix                 ,'-1')                  as nexsuffix           -- 下一层数编码
,coalesce(to_proc_name              ,'-1')                  as to_proc_name        -- 后工序名称
,coalesce(cast(update_new_id as string)    ,'-1')           as update_new_id       -- 更新id号
,coalesce(creation_date             ,'-1')                  as creation_date       -- 创建时间
,coalesce(last_update_date          ,'-1')                  as last_update_date    -- 更新时间
,coalesce(employee_name            ,'-1')                   as employee_name       -- 操作人
,cast(now() as string)                                      as load_time           -- 数据写入时间
,to_date(trunc(stampdatetime,'MM'))                         as pt_m
--,substring(to_date(cast(stampdatetime as string)),1,4 )    as pt_y
from    bi_ods.ods_cux_cux_mes_data_flow_all
```

## 建库建表
```.text
-- 常规建表 row format格式
DROP TABLE IF EXISTS bi_data.dwd_srm_suppliers_list_vl_ds;
CREATE TABLE IF NOT EXISTS bi_data.dwd_srm_suppliers_list_vl_ds
(
  starttime STRING comment'统计日期',
  supplier_code STRING comment'供应商编码',
  supplier_name STRING comment'供应商名称',
  supplier_level STRING comment'供应商等级',
  supplier_lifecycle STRING comment'供应商周期',
  is_strategic_supplier STRING comment'是否战略供应商',
  last_update_date STRING comment'最新更新日期'
)comment 'SRM供应商清单 '
row format
delimited fields terminated by '\001'
lines terminated by '\n';
INVALIDATE METADATA   bi_data.dwd_srm_suppliers_list_vl_ds  ;  -- 刷新表元数据
COMPUTE STATS         bi_data.dwd_srm_suppliers_list_vl_ds  ;  -- 收集表信息
```