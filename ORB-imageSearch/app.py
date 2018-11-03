#!/usr/bin/env python
# coding: utf-8

import asyncio
import time
from operator import itemgetter

import uvloop
from config.config import match_type, site_name, upload_image_path
from mlibs.orb_features import generate_image_feature
from mlibs.orb_matches import knn_match, bf_match
from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import json
from sanic_jinja2 import SanicJinja2
from tinydb import TinyDB

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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
    image_url = request.url + 'static/css/background.jpg'
    response_dict = {
        'site_name': site_name,
        'background_image': image_url
    }
    return response_dict


@app.route("/search", methods=["POST"])
async def search(request):
    upload_image = request.files.get("image")
    if not upload_image:
        raise NotFound(message='not image file')
    image_types = ['image/jpeg', 'image/jpg', 'image/png']
    if upload_image.type not in image_types:
        raise NotFound(message='not image file')
    upload_image_type = upload_image.type.split('/')[-1]
    file_name = str(time.time())[:10] + '.' + upload_image_type
    file_path = upload_image_path + file_name
    with open(file_path,"wb") as f:
        f.write(request.files["image"][0].body)
    results = image_search(file_path)
    image_ids = [result[0] for result in results]
    return json({"result": image_ids})


def image_search(image_path=None):
    """ 图像搜索 """
    global cache_features

    match_results = []
    match_results_append = match_results.append
    search_feature = generate_image_feature(image_path, False)[1]
    for image_uid, feature in cache_features.items():
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


if __name__ == '__main__':
    db = TinyDB('./static/dataset.db')
    table = db.table('feature')
    cache_features = table.all()[0]
    app.run(host='0.0.0.0', port=8000, debug=True)
