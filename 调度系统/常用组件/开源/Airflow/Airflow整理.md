
# Airflow整理

---






## 常见名称解释
- [Data Pipeline]()
```.text
数据管道或者数据流水线，可以理解为贯穿数据处理分析过程中不同工作环节的流程，例如加载不同的数据源，数据加工以及可视化。
```
- [DAGs]()
```.text
是有向非循环图（directed acyclic graphs），可以理解为有先后顺序任务的多个Tasks的组合。图的概念是由节点组成的，有向的意思就是说节点之间是有方向的，转成工业术语我们可以说节点之间有依赖关系；非循环的意思就是说节点直接的依赖关系只能是单向的，不能出现 A 依赖于 B，B 依赖于 C，然后 C 又反过来依赖于 A 这样的循环依赖关系。
每个 Dag 都有唯一的 DagId，当一个 DAG 启动的时候，Airflow 都将在数据库中创建一个DagRun记录，相当于一个日志。
```
- [Task]()
```.text
是包含一个具体Operator的对象，operator实例化的时候称为task。DAG图中的每个节点都是一个任务，可以是一条命令行（BashOperator），也可以是一段 Python 脚本（PythonOperator）等，然后这些节点根据依赖关系构成了一个图，称为一个 DAG。当一个任务执行的时候，实际上是创建了一个 Task实例运行，它运行在 DagRun 的上下文中。
```
- [Connections]()
```.text
是管理外部系统的连接对象，如外部MySQL、HTTP服务等，连接信息包括conn_id／hostname／login／password／schema等，可以通过界面查看和管理，编排workflow时，使用conn_id进行使用
```
- [Pools]()
```.text
用来控制tasks执行的并行数。将一个task赋给一个指定的pool，并且指明priority_weight权重，从而干涉tasks的执行顺序。
```
- [XComs]()
```.text
在airflow中，operator一般是原子的，也就是它们一般是独立执行，不需要和其他operator共享信息。但是如果两个operators需要共享信息，例如filename之类的，则推荐将这两个operators组合成一个operator；如果一定要在不同的operator实现，则使用XComs (cross-communication)来实现在不同tasks之间交换信息。在airflow 2.0以后，因为task的函数跟python常规函数的写法一样，operator之间可以传递参数，但本质上还是使用XComs，只是不需要在语法上具体写XCom的相关代码。
```
- [Trigger Rules]()
```.text
指task的触发条件。默认情况下是task的直接上游执行成功后开始执行，airflow允许更复杂的依赖设置，包括all_success(所有的父节点执行成功)，all_failed(所有父节点处于failed或upstream_failed状态)，all_done(所有父节点执行完成)，one_failed(一旦有一个父节点执行失败就触发，不必等所有父节点执行完成)，one_success(一旦有一个父节点执行成功就触发，不必等所有父节点执行完成)，dummy(依赖关系只是用来查看的，可以任意触发)。
另外，airflow提供了depends_on_past，设置为True时，只有上一次调度成功了，才可以触发。
```
- [Backfill]()
```.text
可以支持重跑历史任务，例如当ETL代码修改后，把上周或者上个月的数据处理任务重新跑一遍。
```




## 参考资料
- [airflow官方文档](https://airflow.apache.org/docs/apache-airflow/stable/database-erd-ref.html)
- [Airflow 入门案例教程](https://blog.csdn.net/helunqu2017/article/details/150018797)










