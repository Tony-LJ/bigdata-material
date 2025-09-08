
# Airflow常见问题整理

---

## Q-1 
- [报错现象]() </br>
![img](imgs/28362484378.png) </br>
![img](imgs/e0e1c570f862d0edf05df90fb61113f4.png) </br>
- [负面影响]() </br>
```.text
DAG Pipeline某些Task的重试机制失效，进而导致该DAG Pipeline整体失败
```
- [原因分析]() </br>
  - 查看airflow安装服务器  </br>
  ![img](imgs/628764357034.png) </br>
```.text
docker inspect e977a011eecc
```
![img](imgs/48574956098.png) </br>


- [解决步骤]() </br>
```.text
docker exec -it -u root 361a43ec1804 /bin/bash
或者：docker exec -it 361a43ec1804 /bin/bash
vi /etc/hosts
填上容器的ip地址与服务器名称(容器ID)
```

## Q-2
- [报错现象]() </br>
- [负面影响]() </br>
```.text

```

- [原因分析]() </br>
```.text

```

- [解决步骤]() </br>
```.text

```


## Q-3
- [报错现象]() </br>
- [负面影响]() </br>
```.text

```

- [原因分析]() </br>
```.text

```

- [解决步骤]() </br>
```.text

```