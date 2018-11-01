# coding: utf-8

import cv2
from config.config import maximum_features, scale_factor


def generate_image_feature(image_path: str) -> tuple:
    """
    生成图像特征点
    :param image_path: 图像路径
    """
    image_uid = image_path[image_path.rfind("/") + 1:][:6]
    images = cv2.imread(image_path)
    orb = cv2.ORB_create(maximum_features, scale_factor)
    (kp, des) = orb.detectAndCompute(images, None)
    feature = des.tolist()
    return image_uid, feature
