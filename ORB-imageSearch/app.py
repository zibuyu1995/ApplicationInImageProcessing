#!/usr/bin/env python
# coding: utf-8

from sanic import Sanic
from sanic.response import json
from until.orb_matches import knn_match, bf_match
from config.config import match_type


app = Sanic(__name__)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/search")
async def search():
    pass


async def image_search(eve_loop, processes_executor, images_features):
    """ 多进程匹配 """
    image_search_tasks = []
    task_append = image_search_tasks.append
    for image_feature in images_feature:
        if match_type == 1:
            task_append(
                eve_loop.run_in_executor(
                    processes_executor, knn_match, image_feature
                )
            )
        else:
            task_append(
                eve_loop.run_in_executor(
                    processes_executor, bf_match, image_path
                )
            )
    task_results, _ = await asyncio.wait(image_feature_tasks)


app.run(host='0.0.0.0', port=8000, debug=True)
