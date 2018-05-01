#coding: utf# -8

import os
import cv2
import numpy as np
from exceptions import Exception


class SeamCarver:
    def __init__(self , filename , out_height , out_width):
        self.filename = filename
        self.out_height = out_height
        self.out_width = out_width
        # 读入图像并转为float64
        if  os.path.exists(self.filename):
            self.image = cv2.imread(filename).astype(np.float64)
        else:
            raise Exception('file not exists')
