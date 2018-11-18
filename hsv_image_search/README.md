# 基于HSV颜色特征的图像搜索引擎

### DP:
* 编写时间: 2018-11-15
* 编写人: Mousse
* 联系邮箱: zibuyu1995@gmail.com

### 系统环境:
* python3.6
* opencv 3.4.2

### 文件结构:
```
├── README.md
├── app.py  # flask 运行代码
├── config
│   ├── __init__.py
│   └── config.py  # 配置文件
├── generate_index.py  # 索引文件生成
├── mlibs
│   ├── __init__.py
│   ├── hsv_features.py # HSV 特征提取
│   └── image_match.py  # HSV 特征匹配
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
# 常规运行
python app.py
# gunicorn 运行
gunicorn --workers=2 --bind=0.0.0.0:5555 app:app
```

### 测试:
> GET http://0.0.0.0:5555/

* 环境: macOS
![image](https://user-images.githubusercontent.com/17525759/48668695-1b5efb80-eb2f-11e8-895b-4c9c4c1a6105.png)

### 常见错误处理:
* may have been in progress in another thread when fork() was called.
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

### 备注:
* HSV 算法不适合于颜色不鲜明的图像匹配
* image_bins: （8, 3, 3）：最佳颜色特征点选择
* 有什么问题请联系我: zibuyu1995@gmail.com

### reference
* 数据集下载: https://pan.baidu.com/s/1bnhR65SyfONoKTK90T57tQ 密码:r0d2
* [flask](http://flask.pocoo.org/docs/0.12/)

