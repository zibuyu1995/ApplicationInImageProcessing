# coding=utf-8
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug import secure_filename
from search.ORBsearcher import Searcher

import cv2
import os

app = Flask(__name__)


# 主页部分
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files['file']
        # 保存图像
        filename = secure_filename(image.filename)
        image.save(os.path.join('./static/query', filename))

        return redirect(url_for('search', filename=filename))

    return render_template('index.html',
                           )


# 搜索页面部分
@app.route('/searchs/<filename>', methods=['POST', 'GET'])
def search(filename):
    query = cv2.imread('./static/query/%s' % filename)
    # 提取搜索图像的特征点并计算特征值（100个点）
    orb = cv2.ORB_create(100, 1.2)
    kp1, des1 = orb.detectAndCompute(query, None)
    s = Searcher(des1)
    s.Search()
    results = s.results
    result = results[::-1]
    # 传递参数给html
    return render_template('result.html', result=result, filename=filename)
