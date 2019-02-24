#!/usr/bin/env python
# coding: utf-8

"""
图像切割为100*100小块
"""

import os

import cv2


def equ_cut():
    in_path = './test/girl.png'
    out_directory = './test/cut_images'
    image_ext = os.path.splitext(os.path.basename(in_path))[-1]

    origin_image = cv2.imread(in_path)
    h, w = origin_image.shape[:2]

    for i in range(1, int(h / 100)):
        for j in range(1, int(w / 100)):
            cut_image = origin_image[(i-1)*100:i*100, (j-1)*100:j*100]
            cv2.imwrite(f'{out_directory}/{i}-{j}{image_ext}', cut_image)


if __name__ == '__main__':
    equ_cut()

