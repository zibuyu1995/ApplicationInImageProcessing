# coding: utf-8

import os
from multiprocessing import cpu_count


project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
cpu_count = cpu_count()
redis_address = 'redis://:public@localhost:6379/1'
dataset_path = os.path.join(project_path, 'static/dataset')

maximum_features = 100  # 图像最大特征点
scale_factor = 1.2  # 缩放因子

