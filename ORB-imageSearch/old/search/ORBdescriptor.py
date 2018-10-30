# coding=utf-8
import cv2
import numpy as np


class OrbDescriptor:
    # 蛮力匹配,不做任何筛选。
    def bfdes(self, des1, des2):
        # 保留最大的特征点数目
        # 找到ORB特征点并计算特征值
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        return len(matches)

    # knn筛选匹配点，数据较大的时候建议筛选
    def knndes(self, des1, des2):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)
        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
        return len(good)
