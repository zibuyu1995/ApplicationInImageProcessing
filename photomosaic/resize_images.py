#!/usr/bin/env python
# coding: utf-8

from _libs.resize_images import resize_images
from config import origin_ds_path, resize_ds_path, dimensions


if __name__ == '__main__':
    resize_images(origin_ds_path, resize_ds_path, dimensions)
