# ORB特征提取算法来实现相似图像匹配

### IGNB:
* 编写时间: 2018-11-3
* 编写人: Mousse
* 联系邮箱: taodk@emqx.io

### 系统环境:
* python3.6
* opencv 3.4.2

### 文件结构:
```
├── README.md
├── app.py  # sanic 运行代码
├── config
│   ├── __init__.py
│   └── config.py  # 配置文件
├── generate_index.py  # 索引文件生成
├── mlibs
│   ├── __init__.py
│   ├── orb_features.py # ORB 特征提取
│   └── orb_matches.py  # ORB 特征匹配
├── static
│   ├── dataset  # 数据集
├── dataset.db  # 序列化后数据集(需要执行generate_index.py后生成)
├── templates
│   ├── index.html
│   └── search.html
└── test
    └── 100900.png  # 测试图片
└── requirements.txt # 依赖
```

### 项目运行:
> 创建虚拟环境后请依据场景修改config/config.py 配置

* 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.douban.com/simple/
```

* 生成索引文件
```bash
python generate_index.py
```

* 运行项目
```bash
python app.py
```

### 测试:
> GET http://0.0.0.0:5555/

* 环境: macOS
![image](https://user-images.githubusercontent.com/17525759/47960017-999aa880-e02d-11e8-8769-ec8ddc7effeb.png)

### 常见错误处理:
* may have been in progress in another thread when fork() was called.
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

### 备注:
* ORB 算法不适合于特征点不明显的图像匹配
* maximum_features: 慎重选择数量太大计算量大，太小匹配结果不明显
* sanic: 是一个半成品框架，期待Flask异步
* 后面应该不会再来重构项目，准备向深度学习方向前进
* 有什么问题请联系我: zibuyu1995@gmail.com

### reference
* 数据集下载:
* [sanic](https://sanic.readthedocs.io/)


