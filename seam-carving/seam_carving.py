# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from exceptions import Exception


class SeamCarver(object):
    def __init__(self, filename, out_height, out_width):
        self.filename = filename
        self.out_height = out_height
        self.out_width = out_width
        # 读入图像并转为float64
        if os.path.exists(self.filename):
            self.in_image = cv2.imread(filename).astype(np.float64)
        else:
            raise Exception('image file not exists')
        self.in_height, self.in_width = self.in_image.shape[: 2]
        self.out_image = np.copy(self.in_image)

        self.kernel_x = np.array(
            [[0., 0., 0.], [-1., 0., 1.], [0., 0., 0.]],
            dtype=np.float64
        )
        self.kernel_y_left = np.array(
            [[0., 0., 0.], [0., 0., 1.], [0., -1., 0.]],
            dtype=np.float64
        )
        self.kernel_y_right = np.array(
            [[0., 0., 0.], [1., 0., 0.], [0., -1., 0.]],
            dtype=np.float64
        )

    @staticmethod
    def rotate_image(image, ccw=False):
        """ 旋转图像 """

        h, w, ch = image.shape
        output = np.zeros((w, h, ch))

        if ccw:
            # 逆时针旋转(counter clock wise)
            flip_image = np.fliplr(image)
            for c in range(ch):
                for row in range(h):
                    output[:, row, c] = flip_image[row, :, c]
        else:
            # 顺时针旋转
            for c in range(ch):
                for row in range(h):
                    output[:, h-1-row, c] = image[row, :, c]
        return output

    def seams_carving(self):
        # 计算需要插入行和列的数目
        delta_row = int(self.out_height - self.in_height)
        delta_col = int(self.out_width - self.in_width)

        # 垂直方向
        if delta_col < 0:
            # 垂直方向缩小 todo
            pass
        elif delta_col > 0:
            # 垂直方向放大 todo
            pass
        
        # 水平方向，先旋转再再缩小
        if delta_row < 0:
            # 旋转图像ccw=True 逆时针旋转
            self.out_image = self.rotate_image(self.out_image, ccw=True)
            # 水平方向删除缝隙 todo
        elif delta_row > 0:
            self.out_image = self.rotate_image(self.out_image, ccw=True)
            # 水平方向插入缝隙 todo
