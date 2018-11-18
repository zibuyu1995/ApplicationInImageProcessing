# coding: utf-8

import os
from multiprocessing import cpu_count

site_name = '基于HSV图像搜索引擎'  # 网站标题
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
cpu_count = cpu_count()

upload_image_path = os.path.join(project_path, 'static/uploads/')  # 上传图片保存地址
dataset_db_path = os.path.join(project_path, 'static/dataset.db')  # 序列化后数据集保存地址
dataset_path = os.path.join(project_path, 'static/dataset/')  # 数据集图片保存地址
image_bins = (8, 3, 3)  # HSV所占权重
