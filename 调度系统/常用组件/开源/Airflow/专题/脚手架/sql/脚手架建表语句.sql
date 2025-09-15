-- #####################################################################
-- descri: Airflow自定义多任务脚手架底层核心表:(airflow_dag_task_pipeline、airflow_dag_task_lineage、airflow_dag_task_attribute)
-- author: Tony
-- date: 2025-09-15
-- #####################################################################
-- Airflow DAG Task任务列表
drop table if exists airflow_dag_task_pipeline;
create table if not exists airflow_dag_task_pipeline (
    dag_id varchar(100) not null comment 'dag id',
    task_id varchar(100) not null comment 'task id',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default null comment '创建时间',
    update_by varchar(64) default null comment '更新人',
    update_time datetime default null comment '更新时间',
    primary key (task_id) using btree
) engine=innodb default charset=utf8mb4 comment='airflow dag task任务表';
-- 插入测试数据
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'bi_ads_ads_wip_online_bala_detail_ds', 'tony', '2025-09-15 15:42:32', 'tony', '2025-09-15 15:42:32');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'bi_ads_ads_wip_online_bala_info_ds', 'tony', '2025-09-15 15:42:35', 'tony', '2025-09-15 15:42:35');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'bi_data_dwd_apps_wip_discrete_jobs_v', 'tony', '2025-09-15 15:42:39', 'tony', '2025-09-15 15:42:39');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'bi_data_dwd_cux_mes_online_bala', 'tony', '2025-09-15 15:42:44', 'tony', '2025-09-15 15:42:44');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'bi_data_dws_wip_online_bala_ds', 'tony', '2025-09-15 15:42:49', 'tony', '2025-09-15 15:42:49');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'end', 'tony', '2025-09-15 15:42:52', 'tony', '2025-09-15 15:42:52');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'fine_bi_ads_wip_online_bala_detail_ds', 'tony', '2025-09-15 15:42:55', 'tony', '2025-09-15 15:42:55');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'fine_bi_ads_wip_online_bala_info_ds', 'tony', '2025-09-15 15:42:58', 'tony', '2025-09-15 15:42:58');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'fine_bi_dws_wip_online_bala_ds', 'tony', '2025-09-15 15:43:00', 'tony', '2025-09-15 15:43:00');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'ODS_APPS_WIP_DISCRETE_JOBS_V', 'tony', '2025-09-15 15:43:03', 'tony', '2025-09-15 15:43:03');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'ODS_CUX_MES_ONLINE_BALA_T', 'tony', '2025-09-15 15:43:06', 'tony', '2025-09-15 15:43:06');
INSERT INTO `utc`.`airflow_dag_task_pipeline` (`dag_id`, `task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'start', 'tony', '2025-09-15 15:43:08', 'tony', '2025-09-15 15:43:08');

-- airflow dag task任务依赖关系列表
drop table if exists airflow_dag_task_lineage;
create table if not exists airflow_dag_task_lineage (
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
-- 插入测试数据
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_ads_ads_wip_online_bala_detail_ds', 'fine_bi_ads_wip_online_bala_detail_ds', 'tony', '2025-09-15 15:42:32', 'tony', '2025-09-15 15:42:32');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_ads_ads_wip_online_bala_info_ds', 'fine_bi_ads_wip_online_bala_info_ds', 'tony', '2025-09-15 15:42:35', 'tony', '2025-09-15 15:42:35');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_data_dwd_apps_wip_discrete_jobs_v', 'bi_data_dws_wip_online_bala_ds', 'tony', '2025-09-15 15:42:39', 'tony', '2025-09-15 15:42:39');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_data_dwd_cux_mes_online_bala', 'bi_data_dws_wip_online_bala_ds', 'tony', '2025-09-15 15:42:44', 'tony', '2025-09-15 15:42:44');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_data_dws_wip_online_bala_ds', 'bi_ads_ads_wip_online_bala_detail_ds', 'tony', '2025-09-15 15:42:49', 'tony', '2025-09-15 15:42:49');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_data_dws_wip_online_bala_ds', 'bi_ads_ads_wip_online_bala_info_ds', 'tony', '2025-09-15 15:42:52', 'tony', '2025-09-15 15:42:52');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('bi_data_dws_wip_online_bala_ds', 'fine_bi_dws_wip_online_bala_ds', 'tony', '2025-09-15 15:42:55', 'tony', '2025-09-15 15:42:55');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('fine_bi_ads_wip_online_bala_detail_ds', 'end', 'tony', '2025-09-15 15:42:58', 'tony', '2025-09-15 15:42:58');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('fine_bi_ads_wip_online_bala_info_ds', 'end', 'tony', '2025-09-15 15:43:00', 'tony', '2025-09-15 15:43:00');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('fine_bi_dws_wip_online_bala_ds', 'end', 'tony', '2025-09-15 15:43:03', 'tony', '2025-09-15 15:43:03');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('ODS_APPS_WIP_DISCRETE_JOBS_V', 'bi_data_dwd_apps_wip_discrete_jobs_v', 'tony', '2025-09-15 15:43:06', 'tony', '2025-09-15 15:43:06');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('ODS_CUX_MES_ONLINE_BALA_T', 'bi_data_dwd_cux_mes_online_bala', 'tony', '2025-09-15 15:43:08', 'tony', '2025-09-15 15:43:08');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('start', 'ODS_APPS_WIP_DISCRETE_JOBS_V', 'tony', '2025-09-15 15:43:06', 'tony', '2025-09-15 15:43:06');
INSERT INTO `utc`.`airflow_dag_task_lineage` (`upstream_task_id`, `dwonstream_task_id`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('start', 'ODS_CUX_MES_ONLINE_BALA_T', 'tony', '2025-09-15 15:43:08', 'tony', '2025-09-15 15:43:08');

-- airflow dag task属性表
drop table if exists airflow_dag_task_attribute;
create table if not exists airflow_dag_task_attribute (
    dag_id varchar(100) not null comment 'dag id',
    dag_name varchar(100) default null comment 'dag名称',
    task_id varchar(100) not null comment 'task id',
    task_name varchar(100) default null comment 'task名称',
    task_importance varchar(100) default null comment 'task重要性={p0,p1,p2,p3,p4,p5}',
    task_file_name varchar(100) default null comment 'task脚本文件名称',
    task_file_path varchar(100) default null comment 'task脚本文件路径',
    task_type varchar(100) default null comment 'task作业类型',
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
-- 插入测试数据
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'bi_ads_ads_wip_online_bala_detail_ds', 'WIP在线结存明细表', 'p1', 'bi_ads_ads_wip_online_bala_detail_ds.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:32', 'tony', '2025-09-15 15:42:32');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'bi_ads_ads_wip_online_bala_info_ds', 'WIP在线结存汇总表', 'p1', 'bi_ads_ads_wip_online_bala_info_ds.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:35', 'tony', '2025-09-15 15:42:35');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'bi_data_dwd_apps_wip_discrete_jobs_v', '工厂制造-离散作业表', 'p1', 'spark-common-core-1.0.1-SNAPSHOT-jar-with-dependencies.jar', '/opt/script', 'java', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:39', 'tony', '2025-09-15 15:42:39');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'bi_data_dwd_cux_mes_online_bala', 'WIP在线结存', 'p1', 'bi_data_dwd_cux_mes_online_bala.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:44', 'tony', '2025-09-15 15:42:44');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'bi_data_dws_wip_online_bala_ds', 'WIP在线结存明细表', 'p1', 'bi_data_dws_wip_online_bala_ds.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:49', 'tony', '2025-09-15 15:42:49');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'end', 'pipeline-end', 'p5', 'end.py', '/opt/script', 'python', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:52', 'tony', '2025-09-15 15:42:52');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'fine_bi_ads_wip_online_bala_detail_ds', 'WIP在线结存明细表推送FineBI', 'p1', 'fine_bi_ads_wip_online_bala_detail_ds.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:55', 'tony', '2025-09-15 15:42:55');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'fine_bi_ads_wip_online_bala_info_ds', 'WIP在线结存汇总表推送FineBI', 'p1', 'fine_bi_ads_wip_online_bala_info_ds.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:42:58', 'tony', '2025-09-15 15:42:58');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'fine_bi_dws_wip_online_bala_ds', 'WIP在线结存表推送FineBI', 'p1', 'fine_bi_dws_wip_online_bala_ds.sql', '/opt/script', 'sql', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:43:00', 'tony', '2025-09-15 15:43:00');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'ODS_APPS_WIP_DISCRETE_JOBS_V', 'WIP_DISCRETE_JOBS抽数任务', 'p1', 'ODS_APPS_WIP_DISCRETE_JOBS_V.sh', '/opt/script', 'shell', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:43:03', 'tony', '2025-09-15 15:43:03');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'ODS_CUX_MES_ONLINE_BALA_T', 'MES_ONLINE_BALA抽数任务', 'p1', 'ODS_CUX_MES_ONLINE_BALA_T.sh', '/opt/script', 'shell', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:43:06', 'tony', '2025-09-15 15:43:06');
INSERT INTO `utc`.`airflow_dag_task_attribute` (`dag_id`, `dag_name`, `task_id`, `task_name`, `task_importance`, `task_file_name`, `task_file_path`, `task_type`, `task_param`, `operator_type`, `remark`, `del_flag`, `create_by`, `create_time`, `update_by`, `update_time`) VALUES ('kw_wip_dag', 'WIP', 'start', 'pipeline-start', 'p5', 'start.py', '/opt/script', 'python', NULL, 'BashOperator', '测试Task', '0', 'tony', '2025-09-15 15:43:08', 'tony', '2025-09-15 15:43:08');
