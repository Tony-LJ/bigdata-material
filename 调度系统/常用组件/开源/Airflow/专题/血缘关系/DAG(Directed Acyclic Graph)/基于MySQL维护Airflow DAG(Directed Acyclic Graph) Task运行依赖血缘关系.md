
# 基于MySQL维护Airflow DAG(Directed Acyclic Graph) Task运行依赖血缘关系

---


## 技术思路
```.text

```

## 库表设计
```.text
1. airflow dag task脚本依赖血缘dag顶点属性表
drop table if exists utc.airflow_dag_task_nodes;
create table if not exists utc.airflow_dag_task_nodes (
    dag_id varchar(100) not null comment 'dag id',
    dag_name varchar(100) default null comment 'dag名称',
    task_id varchar(100) not null primary key  comment 'task id',
    task_name varchar(100) default null comment 'task名称',
    task_file_name varchar(100) default null comment 'task文件名',
    task_file_path varchar(100) default null comment 'task文件路径',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default null comment '创建时间',
    primary key (task_id) using btree
)engine=innodb auto_increment=1 default charset=utf8mb4 comment='airflow dag task脚本依赖血缘dag顶点属性表';

2. airflow dag task脚本依赖血缘dag边关系表
drop table if exists utc.airflow_dag_task_edges; 
create table if not exists utc.airflow_dag_task_edges (
    upstream_task_id varchar(100) not null comment '上游task id',
    dwonstream_task_id varchar(100) not null comment '下游task id',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default null comment '创建时间',
    primary key (upstream_task_id, dwonstream_task_id),
    foreign key (upstream_task_id) references airflow_dag_task_nodes(task_id),
    foreign key (dwonstream_task_id) references airflow_dag_task_nodes(task_id)
)engine=innodb auto_increment=1 default charset=utf8mb4 comment='airflow dag task脚本依赖血缘dag边关系表';

-- DAG依赖关系查询
select n.task_id, 
       n.task_file_name,
       e.dwonstream_task_id
from airflow_dag_task_nodes n
left join airflow_dag_task_edges e on n.task_id = e.upstream_task_id;

------------------------------------------------------------------------------------------------------
3. Airflow DAG Task脚本与实际作业映射关系信息表
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
4. Airflow DAG Task脚本执行情况信息表
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

------------------------------------------------------------------------------------------------------
-- 重要数据数据指标统计SQL


```



















## 参考资料














