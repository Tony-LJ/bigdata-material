-- #####################################################################
-- descri: Airflow自定义多任务脚手架底层核心表
-- author: Tony
-- date: 2025-09-15
-- #####################################################################
-- Airflow DAG Task任务列表
drop table if exists utc.airflow_dag_task_pipeline;
create table if not exists utc.airflow_dag_task_pipeline (
    dag_id varchar(100) not null comment 'dag id',
    task_id varchar(100) not null comment 'task id',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default null comment '创建时间',
    update_by varchar(64) default null comment '更新人',
    update_time datetime default null comment '更新时间',
    primary key (task_id) using btree
) engine=innodb default charset=utf8mb4 comment='airflow dag task任务表';

-- airflow dag task任务依赖关系列表
drop table if exists utc.airflow_dag_task_lineage;
create table if not exists utc.airflow_dag_task_lineage (
    upstream_task_id varchar(100) not null comment '上游task id',
    dwonstream_task_id varchar(100) not null comment '下游task id',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default null comment '创建时间',
    update_by varchar(64) default null comment '更新人',
    update_time datetime default null comment '更新时间',
    primary key (upstream_task_id,dwonstream_task_id),
    constraint airflow_dag_task_lineage_ibfk_1 foreign key (upstream_task_id) references airflow_dag_task_pipeline (task_id),
    constraint airflow_dag_task_lineage_ibfk_2 foreign key (dwonstream_task_id) references airflow_dag_task_pipeline (task_id)
) engine=innodb default charset=utf8mb4 comment='airflow dag task任务依赖关系表';

-- airflow dag task属性表
drop table if exists utc.airflow_dag_task_attribute;
create table if not exists utc.airflow_dag_task_attribute (
    dag_id varchar(100) not null comment 'dag id',
    dag_name varchar(100) default null comment 'dag名称',
    task_id varchar(100) not null comment 'task id',
    task_name varchar(100) default null comment 'task名称',
    task_importance varchar(100) default null comment 'task重要性={p0,p1,p2,p3,p4,p5}',
    task_file_name varchar(100) default null comment 'task脚本文件名称',
    task_file_path varchar(100) default null comment 'task脚本文件路径',
    task_type varchar(100) default null comment 'task作业类型={BashOperator,PythonOperator,etc}',
    task_param varchar(255) default null comment 'task作业传参(包括：作业资源参数、作业外部传参,etc)',
    operator_type varchar(100) default null comment 'task operator类型',
    remark varchar(255) default null comment '备注',
    del_flag char(1) default '0' comment '删除标记',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default null comment '创建时间',
    update_by varchar(64) default null comment '更新人',
    update_time datetime default null comment '更新时间',
    primary key (dag_id,task_id) using btree
) engine=innodb default charset=utf8mb4 comment='airflow dag task属性表';
