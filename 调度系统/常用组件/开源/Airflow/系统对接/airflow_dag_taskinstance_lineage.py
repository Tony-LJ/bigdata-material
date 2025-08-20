# -*- coding: utf-8 -*-

"""
descr: airflow dag taskInstance 依赖关系解析
author: Tony
date: 2025-08-19
"""

import psycopg2
from psycopg2 import sql

class PostgresqlUtils(object):
    # 可以初始化好，就不需要传值，database建议不传，因为你要查那个表在传的话会更灵活
    def __init__(self,
                 database=None,
                 user="airflow",
                 password="airflow",
                 host="10.53.0.75",
                 port=5432):
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
        self._conn = psycopg2.connect(database=self.database,
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
        except psycopg2.Error as e:
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
    print("Airflow Dag TaskInstance依赖关系解析")
    pg_helper = PostgresqlUtils("airflow")
    pg_helper.get_connection()
    sql_str = "SELECT data FROM public.serialized_dag WHERE dag_id = 'kw_guoshu_incr_day_dag' "
    result = pg_helper.find_all(sql_str)
    print(result)

