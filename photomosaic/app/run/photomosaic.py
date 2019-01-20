#!/usr/bin/env python
# coding: utf-8

from typing import List

from tinydb import TinyDB

from ._libs.hsv_features import get_place_feature
from .config import (
    in_image_path, image_features_path
)


class Photomosaic(object):
    def __init__(self):
        self.features = self._get_features()

    @staticmethod
    def _get_features() -> List:
        db = TinyDB(image_features_path)
        table = db.table('feature')
        return table.all()[0]

    @staticmethod
    def get_origin_place_image_feature():
        origin_features = get_place_feature(
            image=in_image_path,
            bins=(8, 3, 3)
        )
        return origin_features

    def generate_photomosaic(self):
        ...

