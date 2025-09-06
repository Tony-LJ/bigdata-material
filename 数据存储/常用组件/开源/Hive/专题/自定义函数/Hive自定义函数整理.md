
# Hive自定义函数整理

---

## GenericUDF(org.apache.hadoop.hive.ql.udf.generic.GenericUDF)
- [POM]() </br>
```.text
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-exec</artifactId>
    <version>3.1.3</version>
    <scope>provided</scope>
</dependency>
```
- [GenericUDF解析]() </br>
```.text
GenericUDF有三个核心方法需要在自定义函数时重写
1.initialize(ObjectInspector[] objectInspectors) 方法 -> 数据类型判断
这个方法是在 UDF 初始化时调用的。它用于执行一些初始化操作，并且可以用来验证 UDF 的输入参数类型是否正确。参数 objectInspectors 是一个包含输入参数的 ObjectInspector 数组，它描述了每个输入参数的类型和结构。
一般在这个方法中检查输入参数的数量和类型是否满足你的函数的要求。如果输入参数不符合预期，你可以抛出 UDFArgumentException 异常。如果一切正常，你需要返回一个合适的 ObjectInspector 对象，它描述了你的函数返回值的类型。
2.evaluate(DeferredObject[] deferredObjects) 方法 -> 编写业务逻辑
在这个方法中定义真正执行 UDF 逻辑的地方，获取输入的参数，并且根据输入参数执行相应的计算或操作。参数 deferredObjects 是一个包含输入参数的 DeferredObject 数组，你可以通过它来获取实际的输入值。
3.getDisplayString(String[] strings) 方法 -> 定义函数描述信息
这个方法用于描述 UDF 的信息，用于生成可读的查询执行计划（Explain），以便用户了解查询的结构和执行过程。
```

- [GenericUDF使用]() </br>
```.text

```

- [GenericUDF二次开发]() </br>
```.text

```

## UDF(org.apache.hadoop.hive.ql.exec.UDF)
- [POM]() </br>
```.text
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-exec</artifactId>
    <version>3.1.3</version>
    <scope>provided</scope>
</dependency>
```

- [UDF解析]() </br>
```.text

```
- 
- [UDF使用]() </br>
```.text

```

- [UDF二次开发]() </br>
```.text

```















## 参考资料
- [LanguageManual+UDF](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF)