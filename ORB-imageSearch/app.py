#!/usr/bin/env python
# coding: utf-8

import asyncio
from operator import itemgetter

import msgpack
import uvloop
from config.config import (
    dataset_db_path
)
from config.config import match_type
from sanic import Sanic
from sanic.response import json
from until.orb_features import generate_image_feature
from until.orb_matches import knn_match, bf_match

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/search")
async def search():
    pass


def image_search(images_features=None):
    """ 图像搜索 """
    with open(dataset_db_path, 'rb') as db:
        images_feature = msgpack.load(db, use_list=False)
    import time
    a = time.time()
    match_results = []
    match_results_append = match_results.append
    search_feature = generate_image_feature('./static/dataset/100900.png')[1]
    for image_uid, feature in images_feature.items():
        if match_type == 1:
            match_degree = knn_match(search_feature, feature)
            if match_degree < 11:
                continue
        else:
            match_degree = bf_match(search_feature, feature)
            if match_degree < 11:
                continue
        match_results_append((image_uid, match_degree))
    match_results = sorted(match_results, key=itemgetter(1), reverse=True)
    return match_results


app.run(host='0.0.0.0', port=8000, debug=True)
