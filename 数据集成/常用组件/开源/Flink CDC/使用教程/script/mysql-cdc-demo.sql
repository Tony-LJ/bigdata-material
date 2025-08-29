-- ################################################################################
-- # Description: Sync MySQL all
-- # 用法：cd /path/flink-cdc-*
-- #
-- ################################################################################
SET execution.checkpointing.interval = 60s;

drop table if exists  products;
CREATE TABLE products (
      id INT NOT NULL,
      `name`  STRING,
      description STRING,
      create_time TIMESTAMP,
      PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = '10.54.16.113',
    'port' = '3306',
    'username' = 'root',
    'password' = 'Turing123',
    'database-name' = 'bigdata',
    'server-time-zone' = 'Asia/Shanghai',
    'table-name' = 'products'
);
drop table if exists  storage_info;
CREATE TABLE storage_info (
      id INT NOT NULL,
      product_id INT,
      `num` INT,
      PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = '10.54.16.113',
    'port' = '3306',
    'username' = 'root',
    'password' = 'Turing123',
    'database-name' = 'bigdata',
    'server-time-zone' = 'Asia/Shanghai',
    'table-name' = 'storage_info'
);

drop table if exists  product_storage;
CREATE TABLE product_storage (
     product_id INT,
     product_name STRING,
     remain_count INT,
     create_time TIMESTAMP,
     PRIMARY KEY (`product_id`) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://10.54.16.113:3306/bigdata?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC',
    'username' = 'root',
    'password' = 'Turing123',
    'table-name' = 'product_storage',
    'driver' = 'com.mysql.cj.jdbc.Driver',
    'scan.fetch-size' = '200'
);

INSERT INTO product_storage
SELECT a.id AS product_id,a.name AS product_name,b.num AS remain_count,a.create_time
FROM products as a
join storage_info as b on a.id=b.product_id;