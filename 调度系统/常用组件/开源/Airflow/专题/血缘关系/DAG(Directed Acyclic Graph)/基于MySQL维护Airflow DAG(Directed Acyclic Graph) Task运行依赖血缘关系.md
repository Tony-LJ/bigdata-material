
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
  `node_code` varchar(100) DEFAULT NULL COMMENT 'DAG节点编码：1-1、2-1、etc',
  `task_name` varchar(100) DEFAULT NULL COMMENT 'Task名称',
  `operator_type` varchar(100) DEFAULT NULL COMMENT 'Task Operator类型',
  `upstream_dag_id` varchar(100) DEFAULT NULL COMMENT '上游DAG ID',
  `upstream_dag_name` varchar(100) DEFAULT NULL COMMENT '上游DAG名称',
  `upstream_task_id` varchar(100) DEFAULT NULL COMMENT '上游Task Id',
  `upstream_task_name` varchar(100) DEFAULT NULL COMMENT '上游Task名称',
  `dwonstream_dag_name` varchar(100) DEFAULT NULL COMMENT '下游DAG名称',  
  `dwonstream_dag_id` varchar(100) DEFAULT NULL COMMENT '下游DAG Id',
  `dwonstream_task_id` varchar(100) DEFAULT NULL COMMENT '下游Task Id',
  `dwonstream_task_name` varchar(100) DEFAULT NULL COMMENT '下游Task名称', 
  `is_dag_element` char(1) DEFAULT '0' COMMENT '是否满足DAG元素依赖规则',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标记',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dag_id` (`task_id`,`upstream_task_id`,`dwonstream_task_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task脚本依赖血缘关系表'
------------------------------------------------------------------------------------------------------
2. Airflow DAG Task脚本与实际作业映射关系信息表
CREATE TABLE `utc`.`airflow_dag_task_info` (
  `id` bigint(200) NOT NULL AUTO_INCREMENT,
  `dag_id` varchar(100) DEFAULT NULL COMMENT 'DAG ID',
  `dag_name` varchar(100) DEFAULT NULL COMMENT 'DAG名称',
  `task_id` varchar(100) DEFAULT NULL COMMENT 'Task Id',
  `task_name` varchar(100) DEFAULT NULL COMMENT 'Task名称',
  `developer` varchar(100) DEFAULT NULL COMMENT 'Task开发者',
  `importance` varchar(100) DEFAULT NULL COMMENT 'Task重要性程度',
  `task_file_name` varchar(100) DEFAULT NULL COMMENT 'Task脚本文件名称',
  `task_file_path` varchar(100) DEFAULT NULL COMMENT 'Task脚本文件路径',
  `task_type` varchar(100) DEFAULT NULL COMMENT 'Task作业类型',
  `operator_type` varchar(100) DEFAULT NULL COMMENT 'Task Operator类型',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标记',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dag_id` (`task_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task脚本与实际作业映射关系信息表'
------------------------------------------------------------------------------------------------------
3. Airflow DAG Task脚本执行情况信息表
CREATE TABLE `utc`.`airflow_dag_task_execute_info` (
  `id` bigint(200) NOT NULL AUTO_INCREMENT,
  `dag_id` varchar(100) DEFAULT NULL COMMENT 'DAG ID',
  `dag_name` varchar(100) DEFAULT NULL COMMENT 'DAG名称',
  `task_id` varchar(100) DEFAULT NULL COMMENT 'Task Id',
  `task_name` varchar(100) DEFAULT NULL COMMENT 'Task名称',
  `developer` varchar(100) DEFAULT NULL COMMENT 'Task开发者',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',  
  `duration` double(10, 2) DEFAULT NULL COMMENT 'Task运行耗时(s)',
  `error_info` varchar(100) DEFAULT NULL COMMENT '报错信息',
  `is_success` char(1) DEFAULT '0' COMMENT '是否执行成功',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',  
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dag_id` (`task_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task脚本执行情况信息表'
------------------------------------------------------------------------------------------------------
5. Airflow DAG Task脚本上下游DAG拓扑依赖血缘查询表；是不是放到图数据库里面维护更好？
CREATE TABLE `utc`.`airflow_dag_task_dag_dependencies` (
  `id` bigint(200) NOT NULL AUTO_INCREMENT,
  `dag_id` varchar(100) DEFAULT NULL COMMENT 'DAG ID',
  `dag_name` varchar(100) DEFAULT NULL COMMENT 'DAG名称',
  `task_id` varchar(100) DEFAULT NULL COMMENT 'Task Id',
  `task_name` varchar(100) DEFAULT NULL COMMENT 'Task名称',
  `operator_type` varchar(100) DEFAULT NULL COMMENT 'Task Operator类型',
  `upstream_dag_id` varchar(100) DEFAULT NULL COMMENT '上游DAG ID',
  `upstream_dag_name` varchar(100) DEFAULT NULL COMMENT '上游DAG名称',
  `upstream_task_id` varchar(100) DEFAULT NULL COMMENT '上游Task Id',
  `upstream_task_name` varchar(100) DEFAULT NULL COMMENT '上游Task名称',
  `dwonstream_dag_name` varchar(100) DEFAULT NULL COMMENT '下游DAG名称',  
  `dwonstream_dag_id` varchar(100) DEFAULT NULL COMMENT '下游DAG Id',
  `dwonstream_task_id` varchar(100) DEFAULT NULL COMMENT '下游Task Id',
  `dwonstream_task_name` varchar(100) DEFAULT NULL COMMENT '下游Task名称', 
  `is_dag_element` char(1) DEFAULT '0' COMMENT '是否满足DAG元素依赖规则',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标记',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dag_id` (`task_id`,`upstream_task_id`,`dwonstream_task_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task脚本上下游依赖血缘查询表'

------------------------------------------------------------------------------------------------------
-- 重要数据数据指标统计SQL


```



















## 参考资料














