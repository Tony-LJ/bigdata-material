
# 基于MySQL维护Airflow DAG(Directed Acyclic Graph) Task运行依赖血缘关系

---


## 技术思路
```.text

```

## 库表设计
```.text
1. Airflow DAG Task脚本上下游依赖血缘关系表
CREATE TABLE `utc`.`airflow_dag_task_dependency` (
  `id` bigint(200) NOT NULL AUTO_INCREMENT,
  `dag_id` varchar(100) DEFAULT NULL COMMENT 'DAG ID',
  `dag_name` varchar(100) DEFAULT NULL COMMENT 'DAG名称',
  `task_id` varchar(100) DEFAULT NULL COMMENT 'Task Id',
  `task_name` varchar(100) DEFAULT NULL COMMENT 'Task名称',
  `upstream_dag_id` varchar(100) DEFAULT NULL COMMENT '上游DAG ID',
  `upstream_task_id` varchar(100) DEFAULT NULL COMMENT '上游Task Id',
  `dwonstream_dag_id` varchar(100) DEFAULT NULL COMMENT '下游DAG Id',
  `dwonstream_task_id` varchar(100) DEFAULT NULL COMMENT '下游Task Id',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标记',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dag_id` (`task_id`,`upstream_task_id`,`dwonstream_task_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task脚本依赖血缘关系表'
```






## 参考资料














