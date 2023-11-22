### 步骤1：环境准备

确保你的计算机上已经安装了 Python 和 pip 工具。

### 步骤2：安装依赖包

在虚拟环境中运行以下命令安装代码所需的依赖包：

```
pip install -r requirements.txt
```

### 步骤3：输入用户数据

![image-20231116121336448](https://typora-md-bucket.oss-cn-beijing.aliyuncs.com/image-20231116121336448.png)

> 获取url步骤：
>
> 1. 进入国科大在线网站[中国科学院大学网络教学平台网络教学平台 (ucas.edu.cn)](http://mooc.ucas.edu.cn/portal) （推荐使用edge 打开）
>
> 2. 点击右上角“校内登录”
>
> 3. 选择使用手机号登录（Mooc 绑定的手机号与密码，对应account与password）
>
> 4. 登录成功后点击右上角个人空间
>
>    ![image-20231116121702645](https://typora-md-bucket.oss-cn-beijing.aliyuncs.com/image-20231116121702645.png)
>
> 5. 在“我学的课”中找到“硕士学位英语（慕课学习）”，进入后随便点击一小节进入，复制进入后网页的网址，更改url值

### 步骤4：运行代码

在虚拟环境中运行脚本：

```
python main.py
```

### 步骤5：执行结果

根据脚本的提示，输入视频线程数量。脚本会根据输入的线程数量，启动多线程处理视频，并生成相应的输出。

以上步骤完成后，你就成功执行了代码并安装了所需的依赖。
