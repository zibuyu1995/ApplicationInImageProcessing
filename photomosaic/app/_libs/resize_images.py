# coding: utf-8

import os
from cv2 import (
    imread, imwrite, resize, INTER_AREA
)
from typing import AnyStr, List, Tuple


def find_images(dir_path: AnyStr) -> List:
    images_path = []
    images_path_append = images_path.append
    for parent, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                images_path_append(os.path.join(parent, file))
    return images_path


def resize_images(in_dir_path: AnyStr, out_dir_path: AnyStr, dimensions: Tuple[int, int]) -> None:
    """
    :param in_dir_path: 所需剪切图像目录
    :param out_dir_path: 剪切后图像保存目录
    :param dimensions: 所需剪切图像大小(100, 100)
    """
    images_path = find_images(in_dir_path)
    for image_path in images_path:
        image_name = os.path.basename(image_path)
        origin_image = imread(image_path)
        resize_image = resize(origin_image, dimensions, interpolation=INTER_AREA)
        out_image_path = os.path.join(out_dir_path, image_name)
        imwrite(out_image_path, resize_image)
