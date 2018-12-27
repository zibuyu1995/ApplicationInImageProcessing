#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np


def read_image():
    img = cv2.imread('/Users/taodekun/Desktop/qqqq.png')
    h, w = img.shape[:2]
    out_image = np.zeros((h * 100, w * 100, 3), dtype=np.uint8)
    cv2.imshow('out_image', out_image)
    print(img.shape)


if __name__ == '__main__':
    read_image()
