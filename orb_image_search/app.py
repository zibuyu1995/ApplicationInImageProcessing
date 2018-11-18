#!/usr/bin/env python
# coding: utf-8

import time
from operator import itemgetter

from aiocache import SimpleMemoryCache
from aiocache.serializers import JsonSerializer
from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import json
from sanic_jinja2 import SanicJinja2
from tinydb import TinyDB

from config.config import (
    match_type, site_name, upload_image_path,
    cpu_count, knn_match_num, bf_match_num
)
from mlibs.orb_features import generate_image_feature
from mlibs.orb_matches import knn_match, bf_match


app = Sanic(__name__)
app.static('/static', './static')
jinja = SanicJinja2(app)
cache_features = {}


@app.exception(NotFound)
async def ignore_404s(request, exception):
    return json({'code': '404'})


@app.route("/")
@jinja.template('index.html')
async def index(request):
    response_dict = {
        'site_name': site_name,
    }
    return response_dict


@app.route("/search")
@jinja.template('search.html')
async def view_search_result(request):
    cache = SimpleMemoryCache(serializer=JsonSerializer())
    response_dict = await cache.get("response_dict")
    if not response_dict:
        response_dict = {}
    return response_dict


@app.route("/search", methods=["POST"])
@jinja.template('search.html')
async def new_search(request):
    upload_image = request.files.get("image")
    if not upload_image:
        raise NotFound(message='not image file')
    image_types = ['image/jpeg', 'image/jpg', 'image/png']
    if upload_image.type not in image_types:
        raise NotFound(message='not image file')
    upload_image_type = upload_image.type.split('/')[-1]
    file_name = str(time.time())[:10] + '.' + upload_image_type
    file_path = upload_image_path + file_name
    with open(file_path, "wb") as f:
        f.write(request.files["image"][0].body)
    search_results = image_search(file_path)[:5]
    cache = SimpleMemoryCache(serializer=JsonSerializer())
    response_dict = {
        'site_name': site_name,
        'upload_image': file_name,
        'search_results': search_results
    }
    await cache.set("response_dict", response_dict)
    return response_dict


def image_search(image_path=None):
    """ 图像搜索 """
    global cache_features

    match_results = []
    match_results_append = match_results.append
    search_feature = generate_image_feature(image_path, False)[1]
    for image_uid, feature in cache_features.items():
        if match_type == 1:
            # knn 匹配
            match_num = knn_match(search_feature, feature)
            if match_num < knn_match_num:
                # 少于knn_match_num个特征点就跳过
                continue
        else:
            match_num = bf_match(search_feature, feature)
            # 蛮力匹配
            if match_num < bf_match_num:
                # 少于bf_match个特征点就跳过
                continue
        match_results_append((image_uid, match_num))
    match_results = sorted(match_results, key=itemgetter(1), reverse=True)
    return match_results


if __name__ == '__main__':
    db = TinyDB('./static/dataset.db')
    table = db.table('feature')
    cache_features = table.all()[0]
    app.run(host='0.0.0.0', port=5555, workers=cpu_count)
