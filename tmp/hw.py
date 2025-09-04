# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas

def plot_DiGraph(edges, title="有向无环图", node_color='skyblue', figsize=(4, 3), seed=42):
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
    DAG = nx.DiGraph()
    DAG.add_edges_from(edges)
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(DAG, seed=seed)
    nx.draw(DAG, pos, with_labels=True, node_color=node_color,
            node_size=2000, edge_color='gray', font_size=10)
    plt.title(title)
    plt.show()

    return DAG

edges_0 = [
    ('A', 'B'),
    ('C', 'B'),
    ('C', 'D'),
    ('B', 'D'),
    ('A', 'C'),
    ('D', 'A'),
]
import pandas as pd
# edges_df = pd.DataFrame(G.edges(), columns=["Source", "Target"])
DAG = plot_DiGraph(edges_0, title="有向无环图（DAG）")
edges_df = pd.DataFrame(DAG.edges(), columns=["Source", "Target"])
edges_df
