# coding=utf-8

from typing import Tuple, AnyStr
import random
import numpy as np
from numpy import ndarray
import cv2
from ..typedefs import HsvBins, ImageArray


def get_image_feature(image_path, bins: HsvBins) -> Tuple:
    """
    计算图像hsv特征值
    :param image_path:
    :param bins: HSV 所占比重
    """
    image = cv2.imread(image_path)
    image_uid = image_path[image_path.rfind("/") + 1:][:6]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 获取图像中心点, 切割图像
    (h, w) = image.shape[:2]
    (c_x, c_y) = (int(w * 0.5), int(h * 0.5))
    segments = [
        (0, c_x, 0, c_y), (c_x, w, 0, c_y),
        (c_x, w, c_y, h), (0, c_x, c_y, h)
    ]

    # 绘制椭圆轮廊
    (axes_x, axes_y) = (int(w * 0.75 / 2), int(h * 0.75 / 2))
    ellipse_mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.ellipse(
        ellipse_mask, (c_x, c_y), (axes_x, axes_y),
        0.0, 0.0, 360.0, (255, 255, 255), -1
    )

    features = []  # 图像特征值
    features_extend = features.extend
    for (start_x, end_x, start_y, end_y) in segments:
        corner_mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(
            corner_mask, (start_x, start_y),
            (end_x, end_y), 255, -1
        )
        # 逆时针计算图像边角颜色直方图
        corner_mask = cv2.subtract(corner_mask, ellipse_mask)
        image_histogram = calculate_histogram(image, corner_mask, bins)
        features_extend(image_histogram)
    # 计算中心椭圆颜色直方图
    image_histogram = calculate_histogram(image, ellipse_mask, bins)
    features_extend(image_histogram)
    convert_features = np.array(features).astype(float)
    return image_uid, convert_features


def get_place_feature(image: ImageArray, bins: HsvBins=None) -> ImageArray:
    """ 计算图像中某一块像素的hsv值 """

    if not bins:
        bins = (8, 3, 3)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 获取图像中心点, 切割图像
    (h, w) = image.shape[:2]
    (c_x, c_y) = (int(w * 0.5), int(h * 0.5))
    segments = [
        (0, c_x, 0, c_y), (c_x, w, 0, c_y),
        (c_x, w, c_y, h), (0, c_x, c_y, h)
    ]

    # 绘制椭圆轮廊
    (axes_x, axes_y) = (int(w * 0.75 / 2), int(h * 0.75 / 2))
    ellipse_mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.ellipse(
        ellipse_mask, (c_x, c_y), (axes_x, axes_y),
        0.0, 0.0, 360.0, (255, 255, 255), -1
    )

    features = []  # 图像特征值
    features_extend = features.extend
    for (start_x, end_x, start_y, end_y) in segments:
        corner_mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(
            corner_mask, (start_x, start_y),
            (end_x, end_y), 255, -1
        )
        # 逆时针计算图像边角颜色直方图
        corner_mask = cv2.subtract(corner_mask, ellipse_mask)
        image_histogram = calculate_histogram(image, corner_mask, bins)
        features_extend(image_histogram)
    # 计算中心椭圆颜色直方图
    image_histogram = calculate_histogram(image, ellipse_mask, bins)
    features_extend(image_histogram)
    convert_features = np.array(features).astype(float)
    return convert_features


def calculate_histogram(image: ImageArray, mask, bins: HsvBins) -> list:
    """
    计算hsv颜色直方图
    :param image: 输入图像
    :param mask: 计算区域
    :param bins: bins: HSV 所占比重
    """

    hist = cv2.calcHist(
        [image], [0, 1, 2], mask, bins,
        [0, 180, 0, 256, 0, 256]
    )
    # 颜色直方图归一化
    histogram = cv2.normalize(hist, hist).flatten()
    return histogram
