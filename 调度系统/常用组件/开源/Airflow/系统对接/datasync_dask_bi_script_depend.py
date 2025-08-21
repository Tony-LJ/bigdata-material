# -*- coding: utf-8 -*-

"""
descr: 定时同步bi_ods.dask_bi_script_depend到csv
*/5 * * * * /usr/bin/python3 /opt/project/datasync_dask_bi_script_depend.py >> /opt/project/datasync_dask_bi_script_depend.log 2>&1

author: Tony
date: 2025-08-19
"""

from impala.dbapi import connect
import pandas as pd


class ImpalaUtils(object):
    def __init__(self,
                 database=None,
                 user="root",
                 password="",
                 host="10.53.0.71",
                 port=21050):
        self._cursor = None  #游标
        self._conn = None   #链接数据库
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.result = None

    def get_connection(self):
        """
        链接数据库
        :return:
        """
        self._conn = connect(database=self.database,
                                      user=self.user,password=self.password,
                                      host=self.host, port=self.port
                                      )


    def close_connection(self):
        """
        关闭数据库连接
        :return:
        """
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    def execute_sql_params(self, sql, params=None):
        """
        执行一条sql  带参数
        :param sql:
        :param params:
        :return:
        """
        self._cursor = self._conn.cursor()
        try:
            print(f"当前执行sql：{sql}，参数：{params}")
            # 执行语句
            self._cursor.execute(sql, params)
        except connect.Error as e:
            print(f"执行sql：{sql}，出错，错误原因：{e}")

    def execute_method(self, sql, params=None, method_name=None):
        """
        通用执行方法
        :param sql:
        :param params:
        :param method_name:
        :return:
        """
        self.get_connection()
        self.execute_sql_params(sql, params)
        if method_name is not None:
            if "find_one" == method_name:
                self._result = self._cursor.fetchone()
            elif "find_all" == method_name:
                self._result = self._cursor.fetchall()
        self.close_connection()

    def get_columns(self, sql, params=None, method_name=None):
        """
        通用执行方法
        :param sql:
        :param params:
        :param method_name:
        :return:
        """
        self.get_connection()
        self.execute_sql_params(sql, params)
        columns = [desc[0] for desc in self._cursor.description]
        self.close_connection()

        return columns

    def find_one(self, sql, params=None):
        """
        查询单条
        :param sql:
        :param params:
        :return:
        """
        self.execute_method(sql, params=params, method_name="find_one")
        return self._result

    def find_all(self, sql, params=None):
        """
        查询所有数据
        :param sql:
        :param params:
        :return:
        """
        self.execute_method(sql, params=params, method_name="find_all")
        return self._result

    def insert(self, sql, params=None):
        """
        插入
        :param sql:
        :param params:
        :return:
        """
        self.execute_method(sql, params=params)

    def update(self, sql, params=None):
        """
        更新
        :param sql:
        :param params:
        :return:
        """
        self.execute_method(sql, params=params)

    def delete(self, sql, params=None):
        """
        删除
        :param sql:
        :param params:
        :return:
        """
        self.execute_method(sql, params=params)


if __name__ == '__main__':
    print("Impala Airflow Dag TaskInstance依赖关系解析")
    impala_helper = ImpalaUtils("impala")
    impala_helper.get_connection()
    sql_str = "select depend_table, target_table from bi_ods.dask_bi_script_depend group by 1,2"
    results = impala_helper.find_all(sql_str)
    columns = impala_helper.get_columns(sql_str)
    df = pd.DataFrame(results, columns=columns)
    # print(results)
    # print(columns)
    # print(df)
    output_file = '/root/airflow/config/bi_backup/bi_script_depend.csv'
    df.to_csv(output_file, index=False)