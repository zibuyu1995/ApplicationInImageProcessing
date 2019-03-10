#!/usr/bin/env python
# coding: utf-8

from typing import List

import cv2
import numpy as np
from tinydb import TinyDB

from .config import (
    image_features_path
)
from .._libs.hsv_features import get_place_feature
from .._libs.image_match import chi_square


class Photomosaic(object):
    def __init__(self):
        self.features = self._get_features()

    @staticmethod
    def _get_features() -> List:
        db = TinyDB(image_features_path)
        table = db.table('feature')
        return table.all()[0]

    def get_pm(self, origin_image):
        h, w = origin_image.shape[:2]
        new_image = np.zeros((h, w, 3), np.uint8)

        for i in range(1, int(h / 100)):
            for j in range(1, int(w / 100)):
                cut_image = origin_image[(i - 1) * 100:i * 100, (j - 1) * 100:j * 100]
                place_feature = get_place_feature(cut_image)
                match_image = self.img_match(place_feature)
                resize_image = cv2.resize(match_image, (100, 100), interpolation=cv2.INTER_AREA)
                new_image[(i - 1) * 100:i * 100, (j - 1) * 100:j * 100] = resize_image
        cv2.imshow('pm', new_image)

    def img_match(self, search_feature):
        """ 图像搜索 """

        match_results = []
        match_results_append = match_results.append
        for image_uid, feature in cache_features.items():
            distance = chi_square(feature, search_feature)
            match_results_append((image_uid, distance))
        match_results = sorted(match_results, key=itemgetter(1))
        optimal_result = match_results[1][0]
        match_image = cv2.imread(f'../static/origin_images/{optimal_result}')
        return match_image

