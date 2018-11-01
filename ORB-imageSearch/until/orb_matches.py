# coding: utf-8

import cv2
import numpy as np


def knn_match(search_feature, feature):
    """ knn 匹配 """
    search_feature = np.array(search_feature, dtype='uint8')
    feature = np.array(feature, dtype='uint8')
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf_matcher.knnMatch(search_feature, trainDescriptors=feature, k=2)
    good_matches = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    return len(good_matches)


def bf_match(search_feature, feature):
    """ 蛮力匹配(保留最大的特征点数目) """
    search_feature = np.array(search_feature, dtype='uint8')
    feature = np.array(feature, dtype='uint8')
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf_matcher.match(search_feature, feature)
    return len(matches)
