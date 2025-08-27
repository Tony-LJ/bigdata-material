# -*- coding: utf-8 -*-
"""
descr: Airflow自定义配置DAG Task血缘关系
author: tony
date: 2025-08-20
"""

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def topological_sort_kahn(graph):
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in graph if in_degree[u] == 0])
    top_order = []

    while queue:
        u = queue.popleft()
        top_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(top_order) == len(graph):
        return top_order
    else:
        return None  # 图中有环，拓扑排序失败

# 创建图并添加边（有向无环图）
G = nx.DiGraph()
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('E', 'F')]
G.add_edges_from(edges)

# 执行拓扑排序
top_order = topological_sort_kahn(G)
if top_order:
    print("拓扑排序结果:", top_order)
else:
    print("图中存在环，无法进行拓扑排序")

# 绘图
pos = nx.spring_layout(G)  # 使用spring布局算法美化图形位置
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='k', node_size=700, font_size=15, font_weight='bold')
plt.title("DAG with Topological Order")
plt.show()