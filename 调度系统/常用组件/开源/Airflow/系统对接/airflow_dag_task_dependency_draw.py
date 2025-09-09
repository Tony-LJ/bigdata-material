# -*- coding: utf-8 -*-
"""
descr: Airflow DAG Task Dependency绘制
author: Tony
date: 2025-08-20
"""

from pymysql import connect
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pandas


class MysqlUtils(object):
    def __init__(self,
                 database=None,
                 user="root",
                 password="LJkwhadoop2025!",
                 host="10.53.0.71",
                 port=3306):
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

def plot_dag_graph(edges,
                   title="有向无环图",
                   node_color='skyblue',
                   figsize=(4, 3), seed=42):
    """
    绘制有向无环图
    参数:
        edges (list of tuples): 因果边，形如 [('A', 'B'), ('B', 'C')]
        title (str): 图标题
        node_color (str): 节点颜色
        figsize (tuple): 图像大小
        seed (int): 随机种子，控制布局稳定性
    返回:
        networkx.DiGraph: 构建的有向图对象
    """
    dag = nx.DiGraph()
    dag.add_edges_from(edges)
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(dag, seed=seed)
    nx.draw(dag,
            pos,
            with_labels=True,
            node_color=node_color,
            node_size=2000,
            edge_color='gray', font_size=10)
    plt.title(title)
    plt.show()

    return dag


if __name__ == '__main__':
    G = nx.DiGraph()
    print("Mysql Airflow Dag TaskInstance依赖关系绘制")
    mysql_helper = MysqlUtils("mysql")
    mysql_helper.get_connection()
    sql_str = """
    select n.task_id, 
           n.task_file_name,
           e.dwonstream_task_id
    from utc.airflow_dag_task_nodes n
    left join utc.airflow_dag_task_edges e on n.task_id = e.upstream_task_id
    where n.dag_id='kw_wip_dag';
    """
    results = mysql_helper.find_all(sql_str)
    columns = mysql_helper.get_columns(sql_str)
    df = pd.DataFrame(results, columns=columns).drop(columns=['task_file_name'])
    # print(results)
    # print(columns)
    print(df)
    # 开始绘制Airflow DAG Task拓扑关系图

    # for row in df.itertuples(index=True, name='Pandas'):
    #     print(f"Index: {row.Index}, task_id: {row.task_id}, dwonstream_task_id: {row.dwonstream_task_id}")
    #     if row.task_id == 'start':
    #         print("从DAG起点开始遍历")
    # for index, row in df.iterrows():
    #     if row['task_id'] != '':  # 确保有父节点才添加边
    #         G.add_edge(row['task_id'], row['dwonstream_task_id'])
    #
    # print(G.edges())

    # tuples_list = [(row['task_id'], row['dwonstream_task_id']) for index, row in df.iterrows()]
    # print(tuples_list)
    # DAG = plot_dag_graph(tuples_list, title="有向无环图（DAG）")
    # edges_df = pd.DataFrame(DAG.edges(), columns=["task_id", "dwonstream_task_id"])
    # edges_df
    
    for index, row in df.iterrows():
        print(f"Index: {index}, task_id: {row['task_id']}, dwonstream_task_id: {row['dwonstream_task_id']}")
