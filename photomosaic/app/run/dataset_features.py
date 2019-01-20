#!/usr/bin/env python
# coding=utf-8

import asyncio
import glob
import ujson
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

import uvloop
from tinydb import TinyDB

from config import resize_ds_path
from _libs.hsv_features import get_image_feature


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def feature_persistence(task_results: list) -> int:
    """ 图像特征集持久化到key-value数据库 """
    feature_dict = dict(task_result.result() for task_result in task_results)
    db = TinyDB('./static/dataset.db')
    table = db.table('feature')
    table.insert(feature_dict)
    feature_count = len(feature_dict)
    return feature_count


async def generate_image_index(eve_loop, processes_executor):
    """ 多进程生成图像索引 """
    image_bins = (8, 3, 3)
    image_feature_tasks = []
    task_append = image_feature_tasks.append
    for image_path in glob.glob(resize_ds_path + "/*.png"):
        print(image_path)
        task_append(
            eve_loop.run_in_executor(
                processes_executor, get_image_feature, image_path, image_bins
            )
        )
    task_results, _ = await asyncio.wait(image_feature_tasks)
    feature_count = feature_persistence(task_results)
    print(f"{feature_count}幅图像完成索引")


if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers=cpu_count())
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            generate_image_index(event_loop, executor)
        )
    finally:
        event_loop.close()
