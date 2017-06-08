# coding=utf-8
from search.colordescriptor import ColorDescriptor

import glob
import cv2
import pymongo

#mongodb数据库初始化
db = pymongo.MongoClient()
features = db.features
index = db.features.tindex


cd = ColorDescriptor((8, 3, 3))

#glob遍历数据集图片，生成数据集存入MongoDB数据库中
for imagePath in glob.glob("/home/search/static/dataset" + "/*.png"):


	ID = imagePath[imagePath.rfind("/") + 1:]
	imageID =ID[:6]
	image = cv2.imread(imagePath)
	# #提取特征值
	features = cd.describe(image)
	features = [float(f) for f in features]
	f = {"_id":imageID, imageID:features}
        index.insert_one(f)
	print  imageID
