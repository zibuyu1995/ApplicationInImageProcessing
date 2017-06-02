# coding=utf-8
import numpy as np
import pymongo
import cv2
from ORBdescriptor import OrbDescriptor

class Searcher(object):
    def __init__(self,des1):
        self.results ={}
        self.des1 = des1

    def Chi(self):
        r = None
        while True:
            feature = yield r
            id = feature["_id"]
            features = feature[id]
            des2 = np.array(features,dtype="uint8")
            orb = OrbDescriptor()
            #校验
            self.results[id] = orb.knndes(self.des1,des2)
            #不做校验
            #self.results [id] =orb.bfdes(self.des1,des2)



    def Search(self):
        #mongo初始化
        db = pymongo.MongoClient()
        Orbfeatures = db.Orbfeatures
        index = db.Orbfeatures.index
        tindex = index.find()
        #内存小的，不建议直接拷贝到列表中。
        L = []
        L.extend(tindex)
		#协程处理
        chi = self.Chi()
        chi.next()
        for feature in L:
            r = chi.send(feature)
        chi.close()
		#结果排序，返回数值最大的5幅图。
        results = sorted([(v, k) for (k, v) in self.results.items()])
        self.results =results[-5:]
