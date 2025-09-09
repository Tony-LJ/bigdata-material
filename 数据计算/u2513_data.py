# -*- coding: utf-8 -*-
import schedule
import time
from impala.dbapi import connect
from impala.util import as_pandas

def impala_conn_exec_sql(sql):
    conn = connect(host='10.53.0.1',
                   port=21050,
                   user='root', password='szkw.COM202201')
    cur = conn.cursor()
    cur.execute(sql)
    data_list=cur.fetchall()

    return data_list

def job():
    impala_conn_exec_sql("drop table if exists bi_tmp.tmp_oe_order_ds_01")
    print("Hello, this is a scheduled job!")

schedule.every().day.at("17:17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
