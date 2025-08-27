# -*- coding: utf-8 -*-
"""
descr: Airflow自定义配置DAG Task血缘关系
author: tony
date: 2025-08-20
"""

class TaskNode:
    def __init__(self, name, task_function):
        self.name = name
        self.task_function = task_function
        self.dependencies = set()

    def add_dependency(self, dependency):
        self.dependencies.add(dependency)

class DirectedEdge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class DAG:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_edge(self, from_node_name, to_node_name):
        from_node = self.nodes[from_node_name]
        to_node = self.nodes[to_node_name]
        edge = DirectedEdge(from_node, to_node)
        from_node.add_dependency(edge)
        self.edges.append(edge)

    def execute(self, start_node):
        visited = set()

        def dfs(node):
            if node.name in visited:
                return
            visited.add(node.name)
            for edge in node.dependencies:
                dfs(edge.to_node)
            node.task_function()

        start_node = self.nodes[start_node]
        dfs(start_node)

if __name__ == '__main__':
    dag = DAG()

    task_a = TaskNode("A", lambda: print("Task A"))
    task_b = TaskNode("B", lambda: print("Task B"))
    task_c = TaskNode("C", lambda: print("Task C"))
    task_d = TaskNode("D", lambda: print("Task D"))

    dag.add_node(task_a)
    dag.add_node(task_b)
    dag.add_node(task_c)
    dag.add_node(task_d)

    dag.add_edge("A", "B")
    dag.add_edge("A", "C")
    dag.add_edge("B", "D")
    dag.add_edge("C", "D")

    dag.execute("B")
