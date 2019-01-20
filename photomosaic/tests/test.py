#!/usr/bin/env python
# coding: utf-8

import cv2
from math import sqrt
import numpy as np

in_path = ''
out_directory = ''
cut_count = 100
cut_base = int(sqrt(100))

origin_image = cv2.imread(in_path)
h, w = origin_image.shape[:2]
h_d = int(h / cut_base)
w_d = int(w / cut_base)

for i in range(1, cut_base):
    for j in range(1, cut_base):
        cut_image = origin_image[(i - 1) * h_d:i * h_d, (j - 1) * w_d:j * w_d]
        cv2.imwrite(f'{out_directory}/{i}-{j}.png', cut_image)
