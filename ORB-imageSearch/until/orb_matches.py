# coding: utf-8


def knn_match(feature_1, feature_2):
    """ knn 匹配 """
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(feature_1, trainDescriptors=feature_2, k=2)
    good_matches = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    return len(good_matches)


def bf_match(feature_1, feature_2):
    """ 蛮力匹配(保留最大的特征点数目) """

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(feature_1, feature_2)
    return len(matches)



