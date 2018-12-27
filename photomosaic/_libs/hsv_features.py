# coding=utf-8


import numpy as np
import cv2


def get_image_feature(image, bins):
    """
    计算图像hsv特征值
    :param image:
    :param bins:
    :return:
    """

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    features = []

    # 获取图像中心点
    (h, w) = image.shape[:2]
    (cX, cY) = (int(w * 0.5), int(h * 0.5))

    # 逆时针计算特征点
    segments = [
        (0, cX, 0, cY), (cX, w, 0, cY),
        (cX, w, cY, h), (0, cX, cY, h)
    ]
    
    (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
    ellipMask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

    for (startX, endX, startY, endY) in segments:
        cornerMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
        cornerMask = cv2.subtract(cornerMask, ellipMask)
        hist = calculate_histogram(image, cornerMask, bins)
        features.extend(hist)
    hist = calculate_histogram(image, ellipMask, bins)
    features.extend(hist)
    return features


def calculate_histogram(image, mask, bins):
    """
    计算hsv颜色直方图
    :param image:
    :param mask:
    :param bins:
    :return:
    """
    hist = cv2.calcHist(
        [image], [0, 1, 2], mask, bins,
        [0, 180, 0, 256, 0, 256]
    )
    histogram = cv2.normalize(hist, hist).flatten()
    return histogram
