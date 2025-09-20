
# Python语言教程

---

## 变量


## 条件结构


## 数据结构



## 常用术语

- [方法()]()
```.text

```

- [函数(def)]()
```.text

```

- [类(class)]()
```.text

```

- [模块(module)]()
```.text
模块：简单来讲就是一个py文件。里面定义了变量、函数、类、方法等
module_a.py
----------------------------------------------------------------------------
def hello(name:str="surpass")->str:
    return f"Hello, {name}!"

def nationality(nationality:str="China")->str:
    if nationality == "China":
        return "I am Chinese"
    elif nationality == "Japan":
        return "I am Japanese"
    elif nationality == "USA":
        return "I am American"
    else:
        return "I am Astronaut"
----------------------------------------------------------------------------
模块使用：
import module_a

if __name__ == '__main__':
    print(module_a.hello())
    print(module_a.nationality())

```

- [包(package)]()
```.text
包：则是一个文件夹里面可以包含多个模块文件，即在一个文件夹里面可以包含多个py文件
示例：
├─calcuator
│   ├─add.py
│   ├─sub.py
│   ├─__init__.py

```

- [绝对导入(absolute import)]()


- [相对导入(relative import)]()


