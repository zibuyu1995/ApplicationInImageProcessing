#!/usr/bin/env python
# coding: utf-8

from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.route("/")
async def test(request):
    return json({"hello": "world"})

app.run(host='0.0.0.0', port=8000, debug=True)
