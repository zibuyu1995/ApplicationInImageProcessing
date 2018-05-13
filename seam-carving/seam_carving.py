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

    def energer_map(self):
        """ 计算图像能量图 """

        b, g, r = cv2.split(self.out_image)
        # 计算rgb三通道图像差分绝对值求和(深度-1，其他默认)
        r_energy = np.absolute(cv2.Scharr(r, -1, 1, 0)) + np.absolute(cv2.Scharr(r, -1, 0, 1))
        g_energy = np.absolute(cv2.Scharr(g, -1, 1, 0)) + np.absolute(cv2.Scharr(g, -1, 0, 1))
        b_energy = np.absolute(cv2.Scharr(b, -1, 1, 0)) + np.absolute(cv2.Scharr(b, -1, 0, 1))
        return r_energy + g_energy + b_energy

    def seams_removal(self, pixel):
        for dummy in range():
            # 计算能量图
            energy_map = self.calc_energy_map()
            # 动态规划计算最小小能量线 todo

            # 从上到下找到并移除最小接缝
            pass

    def seams_insertion(self, pixel):
        for dummy in range():
            # 计算能量图
            energy_map = self.calc_energy_map()
            # 动态规划计算最小小能量线 todo

            # 从上到下找到并移除最小接缝
            pass

    def seams_carving(self):
        # 计算需要插入行和列的数目
        delta_row = int(self.out_height - self.in_height)
        delta_col = int(self.out_width - self.in_width)

        # 垂直方向
        if delta_col < 0:
            # 垂直方向缩小 todo
            self.seams_removal(-delta_col)
        elif delta_col > 0:
            # 垂直方向放大 todo
            pass
        
        # 水平方向，先旋转再再缩小
        if delta_row < 0:
            # 旋转图像ccw=True 逆时针旋转
            self.out_image = self.rotate_image(self.out_image, ccw=True)
            self.seams_removal(delta_row)
        elif delta_row > 0:
            self.out_image = self.rotate_image(self.out_image, ccw=True)
            # 水平方向插入缝隙
            pass
