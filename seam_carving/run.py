#!/usr/bin/env python
# coding: utf-8

from seam_carving import SeamCarver

if __name__ == '__main__':
    file_path = './test/test.jpg'
    out_height, out_width = 250, 350
    seam_carver = SeamCarver(file_path=file_path, out_height=out_height, out_width=out_width)
