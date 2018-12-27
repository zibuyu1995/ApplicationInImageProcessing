#!/usr/bin/env python
# coding: utf-8

from typing import List, AnyStr

import cv2
import numpy as np
from tinydb import TinyDB

from ._libs.hsv_features import get_image_feature


class Photomosaic(object):
    def __init__(self, origin_image_path: AnyStr):
        self.features = self._get_features()
        self.origin_image_path = origin_image_path

    @staticmethod
    def _get_features() -> List:
        db = TinyDB('./static/dataset.db')
        table = db.table('feature')
        return table.all()[0]

    def read_origin_images(self) -> List:
        origin_features = get_image_feature(
            image=self.origin_image_path,
            bins=(8, 3, 3)
        )
        return origin_features

    def generate_photomosaic(self, out_path: AnyStr):
        origin_image = cv2.imread(self.origin_image_path)
        h, w = origin_image.shape[:2]
        out_image = np.zeros((h * 100, w * 100, 3, d), dtype=np.uint8)
        # features matching todo
        cv2.imwrite('./ass.jpg', out_image)
        return out_image


if __name__ == '__main__':
    photomosaic = Photomosaic(origin_image_path='')
    photomosaic.generate_photomosaic(out_path='')
