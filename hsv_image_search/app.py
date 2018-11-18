#!/usr/bin/env python
# coding=utf-8

import time
from operator import itemgetter

from flask import Flask, render_template, request, abort
from tinydb import TinyDB
from werkzeug.contrib.cache import SimpleCache

from config.config import (
    image_bins, site_name, upload_image_path
)
from mlibs.hsv_features import get_image_feature
from mlibs.image_match import chi_square


app = Flask(__name__)
cache = SimpleCache()


@app.route('/')
def index():
    return render_template('index.html', site_name=site_name)


@app.route("/search")
def view_search_result():
    response_dict = cache.get("response_dict")
    if not response_dict:
        response_dict = {}
    return render_template('search.html', **response_dict)


@app.route("/search", methods=["POST"])
def new_search():
    upload_image = request.files.get("image")
    if not upload_image:
        raise abort(404)
    image_types = ['image/jpeg', 'image/jpg', 'image/png']
    if upload_image.content_type not in image_types:
        raise abort(404)
    upload_image_type = upload_image.content_type.split('/')[-1]
    file_name = str(time.time())[:10] + '.' + upload_image_type
    file_path = upload_image_path + file_name
    upload_image.save(file_path)
    search_results = image_search(file_path)[:5]
    response_dict = {
        'site_name': site_name,
        'upload_image': file_name,
        'search_results': search_results
    }
    cache.set("response_dict", response_dict)
    return render_template('search.html', **response_dict)


def image_search(image_path=None):
    """ 图像搜索 """
    global cache_features

    match_results = []
    match_results_append = match_results.append
    search_feature = get_image_feature(image_path, image_bins)[1]
    for image_uid, feature in cache_features.items():
        distance = chi_square(feature, search_feature)
        match_results_append((image_uid, distance))
    match_results = sorted(match_results, key=itemgetter(1))
    return match_results


if __name__ != '__main__':
    # gunicorn 运行
    db = TinyDB('./static/dataset.db')
    table = db.table('feature')
    cache_features = table.all()[0]


if __name__ == '__main__':
    db = TinyDB('./static/dataset.db')
    table = db.table('feature')
    cache_features = table.all()[0]
    app.run(host='0.0.0.0', port=5555)

