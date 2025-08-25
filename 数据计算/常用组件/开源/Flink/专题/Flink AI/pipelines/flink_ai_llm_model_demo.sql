-- ######################################################
-- descr: Flink2.1 AI+LLM大模型调用
-- author: Tony
-- date: 2025-08-25
-- ######################################################

-- 基于Flink AI能力创建算法模型（CREATE MODEL语法创建一个模型）
CREATE MODEL `compliance_model`
INPUT (text STRING)
OUTPUT (response STRING)
WITH(
    'provider'='openai',
    'endpoint'='https://api.openai.com/v1/llm/v1/chat',
    'api-key'='abcdefg',
    'system_prompt' = '你是电商合规审核员，请判断商品标题是否含有酒精、烟草等敏感内容，仅返回JSON：{"risk":0.0~1.0,"reason":"原因"}',
    'model'='gpt-4o'
);

-- ML_PREDICT函数进行实时推理
SELECT * FROM ML_PREDICT(
    INPUT => TABLE input_table,
    MODEL => MODEL my_model,
    ARGS => DESCRIPTOR(text),
    CONFIG => MAP['async', 'true']
);

-- 其中INPUT代表我们的输入数据，一般是类似下面这样的source table：
CREATE TABLE product_source (
    id   STRING,
    title STRING,
    ts   TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
    WATERMARK FOR ts AS ts - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic'     = 'product_source',
    'properties.bootstrap.servers' = 'localhost:9092',
    'format'    = 'json'
);

-- 定义模型计算结果表
CREATE TABLE risk_sink (
   id      STRING,
   title   STRING,
   risk    DOUBLE,
   reason  STRING
) WITH (
  'connector' = 'kafka',
  'topic'     = 'risk_sink',
  'properties.bootstrap.servers' = 'localhost:9092',
  'format'    = 'json'
);

-- 通过一条SQL启动作业：
INSERT INTO risk_sink
SELECT
    id,
    title,
    CAST(JSON_VALUE(response,'$.risk') AS DOUBLE)  AS risk,
    JSON_VALUE(response,'$.reason')                AS reason
FROM (
     SELECT
         id,
         title,
         ML_PREDICT(compliance_model, title) AS response
     FROM product_source
 ) t;

-- 假如我们的输入数据为：
-- kafka-console-producer.sh --broker-list localhost:9092 --topic product_source
-- >{"id":"1","title":"葡萄汁无酒精"}
-- >{"id":"2","title":"天然香草提取物"}   # LLM 会识别其含酒精
-- >{"id":"3","title":"茅台飞天53度"}     # 高风险

-- 输出结果数据：
-- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic risk_sink --from-beginning
-- >{"id":"2","title":"天然香草提取物","risk":0.92,"reason":"香草提取物通常含酒精"}
-- >{"id":"3","title":"茅台飞天53度","risk":0.99,"reason":"明确含酒精饮品"}

-- 根据官方的文档，Flink对大模型的调用支持异步访问，并且默认打开。
-- 在资源规划上，可以参考Little定律进行资源规划:
-- L：队列槽位（对应max-concurrent-operations）
-- λ：请求速率（对应预期的QPS）
-- W：平均延迟（对应模型的响应时间）

-- Flink 2.1的ML框架已经原生支持「Embedding→向量存储→向量检索→LLM」的RAG链路




