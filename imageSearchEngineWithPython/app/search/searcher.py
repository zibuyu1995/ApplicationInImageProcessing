# coding=utf-8
import numpy as np
import pymongo
import cv2


class Searcher(object):
    def __init__(self, queryFeatures):
        self.results = {}
        self.queryFeatures = queryFeatures

    # 消费者
    def Chi(self):
        r = None
        while True:
            feature = yield r
            id = feature["_id"]
            features = feature[id]
            # 卡方验证
            d = 0.5 * np.sum([((a - b) ** 2) / (a + b + 1e-10)
                              for (a, b) in zip(features, self.queryFeatures)])
            self.results[id] = d

    # 生产者
    def Search(self):
        # 数据库连接
        db = pymongo.MongoClient()
        features = db.features
        index = db.features.tindex

        tindex = index.find()
        L = []
        L.extend(tindex)
        # 协程处理
        chi = self.Chi()
        chi.next()
        for feature in L:
            chi.send(feature)
        chi.close()
        # 结果排序
        results = sorted([(v, k) for (k, v) in self.results.items()])
        self.results = results[:6]
