# coding: utf-8

import os
from multiprocessing import cpu_count

site_name = '基于ORB的图像搜索引擎'  # 网站标题
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
cpu_count = cpu_count()

upload_image_path = os.path.join(project_path, 'static/uploads/')  # 上传图片保存地址
dataset_db_path = os.path.join(project_path, 'static/dataset.db')  # 序列化后数据集保存地址
dataset_path = os.path.join(project_path, 'static/dataset/')  # 数据集图片保存地址
maximum_features = 618  # orb算法获取图像最大特征点
scale_factor = 1.2  # 缩放因子
match_type = 1  # 1 knn, 2 bf 匹配方式
knn_match_num = 15  # knn 最少匹配数(需要依据maximum_features来动态调整)
bf_match_num = 256  # bf 方式最少匹配数(需要依据maximum_features来动态调整)
