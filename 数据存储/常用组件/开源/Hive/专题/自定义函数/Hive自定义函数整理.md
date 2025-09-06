
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
GenericUDF有三个核心方法需要在自定义函数时重写：
1.initialize(ObjectInspector[] objectInspectors) 方法               -> 数据类型判断
这个方法是在 UDF 初始化时调用的。它用于执行一些初始化操作，并且可以用来验证 UDF 的输入参数类型是否正确。参数 objectInspectors 是一个包含输入参数的 ObjectInspector 数组，它描述了每个输入参数的类型和结构。
一般在这个方法中检查输入参数的数量和类型是否满足你的函数的要求。如果输入参数不符合预期，你可以抛出 UDFArgumentException 异常。如果一切正常，你需要返回一个合适的 ObjectInspector 对象，它描述了你的函数返回值的类型。
2.evaluate(DeferredObject[] deferredObjects) 方法                   -> 编写业务逻辑
在这个方法中定义真正执行 UDF 逻辑的地方，获取输入的参数，并且根据输入参数执行相应的计算或操作。参数 deferredObjects 是一个包含输入参数的 DeferredObject 数组，你可以通过它来获取实际的输入值。
3.getDisplayString(String[] strings) 方法                           -> 定义函数描述信息
这个方法用于描述 UDF 的信息，用于生成可读的查询执行计划（Explain），以便用户了解查询的结构和执行过程。
```

- [GenericUDF使用]() </br>
```.text
import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.PrimitiveObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;

/**
 * @descr
 * -- 永久注册
 * create function testAdd as 'AddTest' using jar 'hdfs://hadoop201:8020/test/MyUDF-1.0-SNAPSHOT-jar-with-dependencies.jar';
 * -- 删除注册的函数
 * drop function if exists testAdd;
 * -- 使用该函数
 * select testAdd(1,2);
 * 
 * @author Tony
 * @date 2025-09-05
 * */
public class AddTest extends GenericUDF {

    @Override
    public ObjectInspector initialize(ObjectInspector[] objectInspectors) throws UDFArgumentException {
        // 1.校验参数个数
        if (objectInspectors.length != 2) {
            throw new UDFArgumentException("参数个数有误！");
        }

        // 2.检查第1个参数是否是int类型
        // 判断第1个参数的基本类型
        ObjectInspector num1 = objectInspectors[0];
        if (num1.getCategory() != ObjectInspector.Category.PRIMITIVE) {
            throw new UDFArgumentException("第1个参数不是基本数据类型");
        }

        // 第1个参数类型判断
        PrimitiveObjectInspector temp = (PrimitiveObjectInspector) num1;
        if (PrimitiveObjectInspector.PrimitiveCategory.INT != temp.getPrimitiveCategory()) {
            throw new UDFArgumentException("第1个参数应为INT类型");
        }

        // 2.检查第2个参数是否是int类型
        // 判断第2个参数的基本类型
        ObjectInspector num2 = objectInspectors[1];
        if (num2.getCategory() != ObjectInspector.Category.PRIMITIVE) {
            throw new UDFArgumentException("第2个参数不是基本数据类型");
        }

        // 第2个参数类型判断
        PrimitiveObjectInspector temp2 = (PrimitiveObjectInspector) num2;
        if (PrimitiveObjectInspector.PrimitiveCategory.INT != temp2.getPrimitiveCategory()) {
            throw new UDFArgumentException("第2个参数应为INT类型");
        }

        // 3.设置函数返回值类型（返回一个整型数据）
        return PrimitiveObjectInspectorFactory.javaIntObjectInspector;
    }

    @Override
    public Object evaluate(DeferredObject[] deferredObjects) throws HiveException {
        // 完成两数相加的逻辑计算
        int num1 = Integer.parseInt(deferredObjects[0].get().toString());
        int num2 = Integer.parseInt(deferredObjects[1].get().toString());

        return num1 + num2;
    }

    @Override
    public String getDisplayString(String[] strings) {
        return getStandardDisplayString("AddTest", strings);
    }
}

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
- [Hive之UDF运用](https://developer.aliyun.com/article/1519047)