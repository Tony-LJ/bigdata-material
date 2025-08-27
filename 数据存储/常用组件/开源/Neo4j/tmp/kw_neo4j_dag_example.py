# -*- coding: utf-8 -*-
"""
descr: Airflow自定义配置DAG Task血缘关系
author: tony
date: 2025-08-20
"""

from neo4j import GraphDatabase, basic_auth


class Neo4jManager:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, password))

    def close(self):
        self.driver.close()

    # 节点数据打印方法
    def print_node_data(self, record, alias="n"):
        node = record[alias]
        print(f"identity：{node.element_id}")
        print(f"labels：{list(node.labels)}")
        print(f"properties：{dict(node)}")
        print("-" * 30)

    # 关系数据打印方法
    def print_relationship_data(self, record, alias="r"):
        rel = record[alias]
        print(f"identity：{rel.element_id}")
        print(f"start：{rel.start_node.element_id}")
        print(f"end：{rel.end_node.element_id}")
        print(f"type：{rel.type}")
        print(f"properties：{dict(rel)}")
        print("-" * 30)

    # 1. 创建操作
    def create_operation(self):
        with self.driver.session() as session:
            # 示例1：创建简单节点
            session.run("CREATE (a:Person {name: 'Alice', age: 30})")
            print("创建单个节点完成")

            # 示例2：创建节点及关系
            session.run("""
                CREATE (a:Person {name: 'Alice'})
                CREATE (b:Person {name: 'Bob'})
                CREATE (a)-[r:FRIENDS_WITH {since: 2020}]->(b)
            """)
            print("创建节点及关系完成")

            # 示例3：单语句创建节点和关系
            session.run("""
                CREATE (a:Person {name: 'Alice'})-[:WORKS_AT]->(b:Company {name: 'Tech Corp'})
            """)
            print("单语句创建完成")

            # 示例4：基于已有节点创建关系
            session.run("""
                MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
                CREATE (a)-[r:COLLEAGUE_OF {department: 'Engineering'}]->(b)
            """)
            print("基于已有节点创建关系完成")

            # 示例5：创建双向关系
            session.run("""
                MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
                CREATE (a)-[:KNOWS]->(b), (b)-[:KNOWS]->(a)
            """)
            print("双向关系创建完成\n")

    # 2. 查询操作
    def match_operation(self):
        with self.driver.session() as session:
            # 示例1：查询所有Person节点
            print("查询所有Person节点：")
            result = session.run("MATCH (p:Person) RETURN p")
            for record in result:
                self.print_node_data(record, "p")

            # 示例2：查询特定属性节点
            print("\n查询名为Alice的节点：")
            result = session.run("MATCH (p:Person {name: 'Alice'}) RETURN p")
            for record in result:
                self.print_node_data(record, "p")

            # 示例3：查询节点及其关系
            print("\n查询Alice的KNOWS关系：")
            result = session.run("""
                MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person)
                RETURN a, r, b
            """)
            for record in result:
                print("--- 节点A ---")
                self.print_node_data(record, "a")
                print("--- 关系R ---")
                self.print_relationship_data(record, "r")
                print("--- 节点B ---")
                self.print_node_data(record, "b")

            # 示例4：返回特定属性
            print("\n返回姓名和年龄：")
            result = session.run("MATCH (p:Person) RETURN p.name, p.age")
            for record in result:
                print(f"{record['p.name']} - {record['p.age']}")

            # 示例5：条件过滤
            print("\n年龄大于25的人：")
            result = session.run("MATCH (p:Person) WHERE p.age > 25 RETURN p.name, p.age")
            for record in result:
                print(f"{record['p.name']} - {record['p.age']}")

            # 示例6：双向关系查询
            print("\n查询双向KNOWS关系：")
            result = session.run("""
                MATCH (a:Person {name: 'Alice'})-[r1:KNOWS]->(b:Person {name: 'Bob'})
                MATCH (b)-[r2:KNOWS]->(a)
                RETURN a, r1, b, r2
            """)
            for record in result:
                self.print_node_data(record, "a")
                self.print_relationship_data(record, "r1")
                self.print_node_data(record, "b")
                self.print_relationship_data(record, "r2")

            # 示例7：多关系类型匹配
            print("\n模糊匹配关系类型：")
            result = session.run("""
                MATCH (a:Person {name: 'Alice'})-[:KNOWS|WORKS_WITH]->(b)
                RETURN b.name
            """)
            for record in result:
                print(record["b.name"])

            # 示例8：分页查询
            print("\n限制返回3条数据：")
            result = session.run("MATCH (p:Person) RETURN p.name LIMIT 3")
            for record in result:
                print(record["p.name"])

            print("\n跳过1条后返回3条数据：")
            result = session.run("MATCH (p:Person) RETURN p.name SKIP 1 LIMIT 3")
            for record in result:
                print(record["p.name"])

    # 3. 更新操作
    def update_operation(self):
        with self.driver.session() as session:
            # 示例1：更新节点属性
            print("\n更新Alice的年龄：")
            result = session.run("""
                MATCH (n:Person {name: 'Alice'})
                SET n.age = 31
                RETURN n
            """)
            for record in result:
                self.print_node_data(record, "n")

            # 示例2：添加新属性
            print("\n为Bob添加邮箱：")
            result = session.run("""
                MATCH (n:Person {name: 'Bob'})
                SET n.email = 'bob@example.com'
                RETURN n
            """)
            for record in result:
                self.print_node_data(record, "n")

            # 示例3：批量更新属性
            print("\n批量更新Bob的属性：")
            result = session.run("""
                MATCH (n:Person {name: 'Bob'})
                SET n.age = 45, n.city = 'Shanghai', n.job = 'Engineer'
                RETURN n
            """)
            for record in result:
                self.print_node_data(record, "n")

            # 示例4：删除属性
            print("\n删除Alice的年龄属性：")
            result = session.run("""
                MATCH (n:Person {name: 'Alice'})
                REMOVE n.age
                RETURN n
            """)
            for record in result:
                self.print_node_data(record, "n")

            # 示例5：修改标签
            print("\n修改Bob的标签为User：")
            result = session.run("""
                MATCH (n:Person {name: 'Bob'})
                REMOVE n:Person
                SET n:User
                RETURN n
            """)
            for record in result:
                self.print_node_data(record, "n")

            # 示例6：更新关系属性
            print("\n更新关系的since属性：")
            result = session.run("""
                MATCH (:Person {name: 'Alice'})-[r:KNOWS]->(:User {name: 'Bob'})
                SET r.since = 2021
                RETURN r
            """)
            for record in result:
                self.print_relationship_data(record, "r")

    # 4. 删除操作
    def delete_operation(self):
        with self.driver.session() as session:
            # 示例1：删除指定关系
            print("\n删除Alice和Bob之间的KNOWS关系：")
            session.run("""
                MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:User {name: 'Bob'})
                DELETE r
            """)
            print("关系删除完成")

            # 示例2：删除所有KNOWS关系
            print("\n删除所有KNOWS关系：")
            session.run("MATCH ()-[r:KNOWS]->() DELETE r")
            print("关系批量删除完成")

            # 示例3：删除节点（含所有关系）
            print("\n删除Alice节点及所有关系：")
            session.run("MATCH (n:Person {name: 'Alice'}) DETACH DELETE n")
            print("节点删除完成")

            # 示例4：删除孤立节点
            print("\n删除孤立节点：")
            session.run("MATCH (n) WHERE NOT EXISTS((n)--()) DELETE n")
            print("孤立节点删除完成")

            # 示例5：清空数据库
            print("\n清空所有数据：")
            session.run("MATCH (n) DETACH DELETE n")
            print("数据库已清空")

    # 5. 合并操作（MERGE）
    def merge_operation(self):
        with self.driver.session() as session:
            # 示例1：确保节点存在
            print("\n确保Alice节点存在：")
            result = session.run("MERGE (p:Person {name: 'Alice'}) RETURN p")
            for record in result:
                self.print_node_data(record, "p")

            # 示例2：创建或更新节点属性
            print("\n确保Bob节点存在并设置年龄：")
            result = session.run("""
                MERGE (p:Person {name: 'Bob'})
                SET p.age = 30
                RETURN p
            """)
            for record in result:
                self.print_node_data(record, "p")

            # 示例3：区分创建和更新操作
            print("\n使用ON CREATE/MATCH：")
            result = session.run("""
                MERGE (p:Person {name: 'Charlie'})
                ON CREATE SET p.created = datetime()
                ON MATCH SET p.lastSeen = datetime()
                RETURN p
            """)
            for record in result:
                self.print_node_data(record, "p")

            # 示例4：确保关系存在
            print("\n确保Alice和Bob的朋友关系存在：")
            result = session.run("""
                MERGE (a:Person {name: 'Alice'})
                MERGE (b:Person {name: 'Bob'})
                MERGE (a)-[r:FRIENDS_WITH]->(b)
                RETURN a, r, b
            """)
            for record in result:
                self.print_node_data(record, "a")
                self.print_relationship_data(record, "r")

            # 示例5：合并带属性的关系
            print("\n确保带属性的关系存在：")
            result = session.run("""
                MERGE (a:Person {name: 'Alice'})
                MERGE (b:Person {name: 'Bob'})
                MERGE (a)-[r:WORKS_WITH {since: 2022}]->(b)
                RETURN r
            """)
            for record in result:
                self.print_relationship_data(record, "r")


if __name__ == "__main__":
    # 初始化连接（请根据实际情况修改连接参数）
    manager = Neo4jManager(
        uri="bolt://10.53.0.76:18802",
        username="neo4j",
        password="neo4jrag"
    )

    # 执行各操作（可根据需要注释/取消注释）
    manager.create_operation()
    manager.match_operation()
    manager.update_operation()
    manager.delete_operation()
    manager.merge_operation()

    # 关闭连接
    manager.close()
    print("\n操作完成，连接已关闭")
