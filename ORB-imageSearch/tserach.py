# coding=utf-8
import cv2
import numpy as np
import pymongo
from search.ORBsearcher import Searcher
import time

start = time.time()
img = cv2.imread('test33.png')
#计算并提取特征值
orb = cv2.ORB_create(100,1.2)
kp1,des1 = orb.detectAndCompute(img,None)
#实例化
s = Searcher(des1)
s.Search()
results = s.results
#列表反转
print results[::-1]
print("所用时间{}".format(time.time() - start))
