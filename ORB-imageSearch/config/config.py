# coding: utf-8

import os
from multiprocessing import cpu_count

site_name = '基于ORB的图像搜索引擎'
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
cpu_count = cpu_count()

upload_image_path = os.path.join(project_path, 'static/uploads/')
dataset_db_path = os.path.join(project_path, 'static/dataset.db')
dataset_path = os.path.join(project_path, 'static/dataset/')
maximum_features = 618  # 图像最大特征点
scale_factor = 1.2  # 缩放因子
match_type = 1  # 1 knn, 2 bf


