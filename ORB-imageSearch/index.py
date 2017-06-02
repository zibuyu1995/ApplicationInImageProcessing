# coding=utf-8
import glob
import cv2
import numpy as np
import pymongo
import time

#mongodb数据库初始化
db = pymongo.MongoClient()
Orbfeatures = db.Orbfeatures
index = db.Orbfeatures.index


#glob遍历文件夹图片
#路径需要更改
for imagePath in glob.glob("/root/web/ORBsearchs/static/dataset" + "/*.png"):
	ID = imagePath[imagePath.rfind("/") + 1:]
	imageID =ID[:6]
	images = cv2.imread(imagePath)
	#提取搜索图像的特征点并计算特征值（100个点）
	orb = cv2.ORB_create(100,1.2)
	(kp,des) = orb.detectAndCompute(images, None)
	#np数据转列表
	feature = des.tolist()

	f = {"_id":imageID, imageID:feature}
	#插入记录
	index.insert_one(f)
	print  imageID
