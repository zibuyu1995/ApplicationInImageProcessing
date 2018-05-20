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

        # 定义核算子
        self.kernel_x = np.array([[0., 0., 0.], [-1., 0., 1.], [0., 0., 0.]], dtype=np.float64)
        self.kernel_y_left = np.array([[0., 0., 0.], [0., 0., 1.], [0., -1., 0.]], dtype=np.float64)
        self.kernel_y_right = np.array([[0., 0., 0.], [1., 0., 0.], [0., -1., 0.]],
                                       dtype=np.float64)

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
                    output[:, h - 1 - row, c] = image[row, :, c]
        return output

    def energy_map(self):
        """ 计算图像能量图 """

        b, g, r = cv2.split(self.out_image)
        # 计算rgb三通道图像差分绝对值求和(深度-1，其他默认)
        r_energy = np.absolute(cv2.Scharr(r, -1, 1, 0)) + np.absolute(cv2.Scharr(r, -1, 0, 1))
        g_energy = np.absolute(cv2.Scharr(g, -1, 1, 0)) + np.absolute(cv2.Scharr(g, -1, 0, 1))
        b_energy = np.absolute(cv2.Scharr(b, -1, 1, 0)) + np.absolute(cv2.Scharr(b, -1, 0, 1))
        return r_energy + g_energy + b_energy

    def calc_neighbor_matrix(self, kernel):
        """ 相邻矩阵计算 """
        b, g, r = cv2.split(self.out_image)

        # 图像卷积计算
        convolution_abs = [np.absolute(cv2.filter2D(b, -1, kernel=kernel)),
            np.absolute(cv2.filter2D(g, -1, kernel=kernel)),
            np.absolute(cv2.filter2D(r, -1, kernel=kernel))]
        output = sum(convolution_abs)
        return output

    def cumulative_map_forward(self, energy_map):
        """ 累加能量图之前 """

        matrix_x = self.calc_neighbor_matrix(self.kernel_x)
        matrix_y_left = self.calc_neighbor_matrix(self.kernel_y_left)
        matrix_y_right = self.calc_neighbor_matrix(self.kernel_y_right)

        h, w = energy_map.shape
        output = np.copy(energy_map)
        for row in range(1, h):
            for col in range(w):
                if col == 0:
                    e_right = output[row - 1, col + 1] + matrix_x[row - 1, col + 1] + \
                              matrix_y_right[row - 1, col + 1]
                    e_up = output[row - 1, col] + matrix_x[row - 1, col]
                    output[row, col] = energy_map[row, col] + min(e_right, e_up)
                elif col == n - 1:
                    e_left = output[row - 1, col - 1] + matrix_x[row - 1, col - 1] + matrix_y_left[
                        row - 1, col - 1]
                    e_up = output[row - 1, col] + matrix_x[row - 1, col]
                    output[row, col] = energy_map[row, col] + min(e_left, e_up)
                else:
                    e_left = output[row - 1, col - 1] + matrix_x[row - 1, col - 1] + matrix_y_left[
                        row - 1, col - 1]
                    e_right = output[row - 1, col + 1] + matrix_x[row - 1, col + 1] + matrix_y_right[row - 1, col + 1]
                    e_up = output[row - 1, col] + matrix_x[row - 1, col]
                    output[row, col] = energy_map[row, col] + min(e_left, e_right, e_up)
        return output

    @staticmethod
    def find_seam(cumulative_map):
        """
        找到接缝, 从下到上生成接缝
        """
        h, w = cumulative_map.shape
        output = np.zeros((h,), dtype=np.uint32)
        output[-1] = np.argmin(cumulative_map[-1])
        for row in range(h - 2, -1, -1):
            # 从图像底部到顶部回溯找到最小接缝
            prv_x = output[row + 1]
            if prv_x == 0:
                output[row] = np.argmin(cumulative_map[row, : 2])
            else:
                output[row] = np.argmin(cumulative_map[row, prv_x - 1: min(prv_x + 2, n - 1)]) + prv_x - 1
        return output

    def seams_removal(self, pixel):
        for dummy in range(pixel):
            # 计算能量图
            energy_map = self.calc_energy_map()
            # 动态规划计算最小小能量线 todo
            cumulative_map = self.cumulative_map_forward(energy_map)
            seam_idx = self.find_seam(cumulative_map)
            # 从上到下找到并移除最小接缝
            pass

    def seams_insertion(self, pixel):
        for dummy in range(pixel):
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
