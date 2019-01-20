# coding: utf-8

import numpy as np


def chi_square(query_feature, match_feature) -> float:
    """
    卡方校验
    :param query_feature: 搜索图像
    :param match_feature: 匹配图像
    :return: 卡方距离
    """

    distance = 0.5 * np.sum(
        [((a - b) ** 2) / (a + b + 1e-10)
         for (a, b) in zip(match_feature, query_feature)]
    )
    return float(distance)


