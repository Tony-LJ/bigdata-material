
# requirements.txt整理

---

## 介绍
```.text
requirements.txt 文件是 Python 项目中用来管理依赖项的常用方式。它允许列出项目所需的所有 Python 包及其版本，以便自己或其他人可以轻松地在新的环境中安装相同的依赖项，确保项目能够在不同的环境中保持一致性。
```

## requirements.txt的内容
```.text
每行通常包含一个包名和（可选的）版本号。
版本号可以使用 == 指定精确版本，或使用 >= 指定最低版本。
注释以 # 开头，它们将被 pip 忽略。
可以使用 -i 选项来指定 Python 包的索引 URL（即 PyPI 镜像），以便从指定的源安装包。
可以使用 -r 选项来包含另一个 requirements.txt 文件的内容。
在实际项目中，requirements.txt 文件的内容将根据你的项目的具体需求来确定。通常，你会在项目开始时创建一个基本的 requirements.txt 文件，并在项目发展过程中根据需要添加或更新依赖项。
```

## 生成 requirements.txt 文件
```.text
1、手动创建：你可以手动创建一个 requirements.txt 文件，并在其中列出你的项目所需的包和版本。
2、使用 pip freeze：如果你已经在一个环境中安装了所有依赖项，你可以使用 pip freeze 命令来生成 requirements.txt 文件。这将会列出当前环境中安装的所有包及其版本。
pip freeze > requirements.txt
3、pipreqs 是一个工具，它可以扫描你的项目目录并自动生成 requirements.txt 文件。
首先，你需要安装 pipreqs：
pip install pipreqs
然后，在项目根目录下运行 pipreqs：
pipreqs ./ --savepath requirements.txt
```

## 使用 requirements.txt 文件
```.text
安装依赖项：当你或其他人需要在新的环境中设置项目时，可以使用 pip 和 requirements.txt 文件来安装所有必要的依赖项。只需运行以下命令：
pip install -r requirements.txt
确保一致性：通过使用 requirements.txt 文件，你可以确保项目的所有依赖项都在团队成员之间保持一致。当新成员加入项目或当你想在不同的环境中设置项目时，只需运行上述命令即可。
版本控制：将 requirements.txt 文件添加到版本控制系统中（如 Git），这样你可以跟踪依赖项的变化，并在需要时回滚到以前的版本。
考虑使用虚拟环境：为了避免不同项目之间的依赖项冲突，建议使用虚拟环境（如 venv、virtualenv 或 conda）来隔离每个项目的依赖项。在虚拟环境中，你可以为每个项目单独安装其所需的依赖项。
```


## 示例
- [示例requirements.txt文件]()
  ```.text
    # 精确指定版本
    numpy==1.21.0  
    pandas==1.3.0
    
    # 指定最低版本
    scipy>=1.0.0
    
    # 不指定版本，则安装最新版本
    matplotlib
    
    # 可以包含其他选项，如安装源
    # -i 参数用于指定 Python 包的索引 URL
    # 例如，使用清华大学的 PyPI 镜像
    -i https://pypi.tuna.tsinghua.edu.cn/simple  
    requests
    
    # 可以包含多个源
    # 注意：这只是一个示例，不推荐在 requirements.txt 中混合使用多个源
    # 通常，我们会在命令行中使用 --index-url 或 --extra-index-url 参数
    # --index-url https://pypi.tuna.tsinghua.edu.cn/simple
    # requests
    
    # 也可以包含子依赖文件
    # 例如，使用 -r 引入另一个 requirements 文件
    -r requirements-dev.txt
    
    # 注释行以 # 开头，将被 pip 忽略
    # 这里是一个注释
  
  
  ```
```.text
请注意以下几点：
每行通常包含一个包名和（可选的）版本号。
版本号可以使用 == 指定精确版本，或使用 >= 指定最低版本。
注释以 # 开头，它们将被 pip 忽略。
可以使用 -i 选项指定 Python 包的索引 URL（即 PyPI 镜像），可从指定的源安装包。
可以使用 -r 选项来包含另一个 requirements.txt 文件的内容。
在实际项目中，requirements.txt 文件的内容将根据你的项目的具体需求来确定。通常，你会在项目开始时创建一个基本的 requirements.txt 文件，并在项目发展过程中根据需要添加或更新依赖项。
```
