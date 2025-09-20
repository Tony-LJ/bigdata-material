
# Python项目打包整理

---


## python setuptools打包
```.text
作为项目的开发者，你的目标不仅仅是让代码能够运行，更是要让它变得可分发、可安装、可复用。setup.py 就是实现这一目标的核心工具。
```
### 为什么要创建 setup.py？
```.text
1.标准化安装：让任何人都能用一句 pip install -e . 来安装你的项目，而不是去手动复制文件、猜测依赖。
2.依赖管理：在文件中明确声明你的项目依赖哪些第三方库（如 requests, numpy）。pip 在安装你的项目时会自动处理这些依赖。
3.创建命令行工具：可以将你代码中的某个函数直接变成一个可以在终端（Terminal/Shell）里运行的命令。
4.发布到 PyPI：如果你想让全世界的开发者都能通过 pip install your-project-name 安装你的项目，setup.py 是必不可少的一步。
```












## 参考资料
- [Python项目打包之钥:setup.py全方位指南](https://blog.csdn.net/2402_86492143/article/details/151183604)
- [Python包分发终极指南：深入掌握setuptools打包技术](https://blog.csdn.net/weixin_63779518/article/details/148930592)




