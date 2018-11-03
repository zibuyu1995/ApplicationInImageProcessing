# coding: utf-8

import cv2
import msgpack
from config.config import maximum_features, scale_factor


def generate_image_feature(image_path: str, is_dumps: bool) -> tuple:
    """
    生成图像特征点
    :param is_dumps: 是否压缩
    :param image_path: 图像路径
    """
    image_uid = image_path[image_path.rfind("/") + 1:][:6]
    images = cv2.imread(image_path)
    orb = cv2.ORB_create(maximum_features, scale_factor)
    (kp, des) = orb.detectAndCompute(images, None)
    if is_dumps:
        feature = des.tolist()
    else:
        feature = des
    return image_uid, feature
