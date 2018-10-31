# coding=utf-8
"""
Time    : 2018-10-30
Author  : Mousse
email: zibuyu1995@gmail.com
"""

import asyncio
import glob
import ujson
from concurrent.futures import ProcessPoolExecutor

import cv2
import uvloop
from config.config import (
    dataset_path, dataset_db_path,
    cpu_count, maximum_features, scale_factor
)


def generate_image_feature(image_path: str) -> tuple:
    """
    生成图像特征点
    :param image_path: 图像路径
    """
    image_uid = image_path[image_path.rfind("/") + 1:][:6]
    images = cv2.imread(image_path)
    orb = cv2.ORB_create(maximum_features, scale_factor)
    (kp, des) = orb.detectAndCompute(images, None)
    feature = ujson.dumps(des.tolist())
    return image_uid, feature


def feature_persistence(task_results: list) -> int:
    """ 图像特征集持久化到key-value数据库 """

    feature_count = 0
    # todo
    return feature_count


async def generate_image_index(eve_loop, processes_executor):
    """ 多进程生成图像索引 """
    image_feature_tasks = []
    task_append = image_feature_tasks.append
    for image_path in glob.glob(dataset_path + "/*.png"):
        task_append(
            eve_loop.run_in_executor(
                processes_executor, generate_image_feature, image_path
            )
        )
    task_results, _ = await asyncio.wait(image_feature_tasks)
    feature_count = feature_persistence(task_results)
    print(f"{feature_count}幅图像完成索引")


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    executor = ProcessPoolExecutor(max_workers=cpu_count)
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            generate_image_index(event_loop, executor)
        )
    finally:
        event_loop.close()
