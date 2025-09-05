
# Spark开发技巧整理

---

## Spark UDF函数定义、注册与使用
```.text
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.functions;

public static void main(String[] args) {

    UDF1<BigDecimal, Double> numberToDouble = new UDF1<BigDecimal, Double>() {
        @Override
        public Double call(BigDecimal number) throws Exception {
            return number.doubleValue();
        }
    }

    spark.udf().register("numberToDouble", numberToDouble, DataTypes.DoubleType);
   
}
```

























## 参考资料
