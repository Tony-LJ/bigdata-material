
# BashOperator整理

---

## 调度Spark Jar作业
```.text
OdsQeOrderLinesAllSyncPipeline = BashOperator(
    task_id= "OdsQeOrderLinesAllSyncPipeline",
    depends_on_past=False,
    bash_command= f'''ssh root@10.53.0.71 " $SPARK_HOME/bin/spark-submit --master yarn --queue root --deploy-mode cluster --num-executors 18 --executor-memory 10g --executor-cores 10 --conf spark.dynamicAllocation.maxExecutors=100 --class org.apache.common.OdsQeOrderLinesAllSyncPipeline /opt/jars/spark-common-core-1.0.1-SNAPSHOT-jar-with-dependencies.jar;" ''' ,
    dag=dag1
)
```