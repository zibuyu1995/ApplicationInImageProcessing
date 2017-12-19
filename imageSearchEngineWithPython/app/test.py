# coding=utf-8
from search.colordescriptor import ColorDescriptor
# from search.searcher import Searcher
from search.searcher import Searcher
import cv2
import time

# glob来搜索图像路径名称

# 设置搜索bin数值
start = time.time()
cd = ColorDescriptor((8, 3, 3))

# 加载需要查询的图像，并且提取特征值
query = cv2.imread("/home/search/nun/20170910.png")
features = cd.describe(query)
s = Searcher(features)
s.Search()
results = s.results
print results

print("Total elapsed time {}".format(time.time() - start))
