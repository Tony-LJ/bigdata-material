
# PythonOperator整理

---

## 调度API接口
```.text
def run_spark_sql_shell(shell_path):
    try:
        url = "http://10.53.0.1:8082/shell/local/command/shellLocalExecute?filePath={}".format(shell_path)
        method = "POST"
        response = requests.post(url)
        if response.status_code not in [200, 201]:
            print(f"请求失败，状态码：{response.status_code}")
            return 1
        else :
            print("状态正常,传入脚本:" + shell_path)
            return 0
        result = response.json()
        print(print(*result, sep='\n'))
    except Exception as e:
        print("error ... ", e)
        return 1
       
HttpApiPipeline = PythonOperator(
    task_id=HttpApiPipeline,
    depends_on_past=False,
--  python_callable=get_invalidate_and_compute_metadata,
    op_kwargs={"table_name":"{}".format(param)},
)
```