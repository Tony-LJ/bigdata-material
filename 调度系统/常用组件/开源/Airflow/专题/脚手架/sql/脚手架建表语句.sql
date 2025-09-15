-- #####################################################################
-- descri: Airflow自定义多任务脚手架底层核心表
-- author: Tony
-- date: 2025-09-15
-- #####################################################################
-- Airflow DAG Task任务列表
CREATE TABLE `utc.airflow_dag_task_pipeline` (
    `dag_id` varchar(100) NOT NULL COMMENT 'dag id',
    `task_id` varchar(100) NOT NULL COMMENT 'task id',
    `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
    `create_time` datetime DEFAULT NULL COMMENT '创建时间',
    `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
    `update_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`dag_id`,`task_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task任务表'

-- Airflow DAG Task任务依赖关系列表
CREATE TABLE `utc.airflow_dag_task_lineage` (
    `upstream_task_id` varchar(100) NOT NULL COMMENT '上游task id',
    `dwonstream_task_id` varchar(100) NOT NULL COMMENT '下游task id',
    `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
    `create_time` datetime DEFAULT NULL COMMENT '创建时间',
    `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
    `update_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`upstream_task_id`,`dwonstream_task_id`),
    KEY `dwonstream_task_id` (`dwonstream_task_id`),
    CONSTRAINT `airflow_dag_task_lineage_ibfk_1` FOREIGN KEY (`upstream_task_id`) REFERENCES `airflow_dag_task_pipeline` (`task_id`),
    CONSTRAINT `airflow_dag_task_lineage_ibfk_2` FOREIGN KEY (`dwonstream_task_id`) REFERENCES `airflow_dag_task_pipeline` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task任务依赖关系表'

-- Airflow DAG Task属性表
CREATE TABLE `utc.airflow_dag_task_attribute` (
    `dag_id` varchar(100) NOT NULL COMMENT 'dag id',
    `dag_name` varchar(100) DEFAULT NULL COMMENT 'DAG名称',
    `task_id` varchar(100) NOT NULL COMMENT 'task id',
    `task_name` varchar(100) DEFAULT NULL COMMENT 'Task名称',
    `task_importance` varchar(100) DEFAULT NULL COMMENT 'Task重要性={p0,p1,p2,p3,p4,p5}',
    `task_file_name` varchar(100) DEFAULT NULL COMMENT 'Task脚本文件名称',
    `task_file_path` varchar(100) DEFAULT NULL COMMENT 'Task脚本文件路径',
    `task_type` varchar(100) DEFAULT NULL COMMENT 'Task作业类型',
    `task_param` varchar(255) DEFAULT NULL COMMENT 'Task作业传参(包括：作业资源参数、作业外部传参,etc)',
    `operator_type` varchar(100) DEFAULT NULL COMMENT 'Task Operator类型',
    `remark` varchar(255) DEFAULT NULL COMMENT '备注',
    `del_flag` char(1) DEFAULT '0' COMMENT '删除标记',
    `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
    `create_time` datetime DEFAULT NULL COMMENT '创建时间',
    `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
    `update_time` datetime DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`dag_id`,`task_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Airflow DAG Task属性表'
