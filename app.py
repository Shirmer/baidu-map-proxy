from flask import Flask, request, Response
import requests
import os
from functools import lru_cache

app = Flask(__name__)

# 百度密钥存在环境变量中（Render 会在后台设置）
BAIDU_AK = os.getenv("BAIDU_MAP_AK")

@lru_cache(maxsize=128)
def fetch_baidu_map(lon, lat, zoom=13, width=800, height=600):
    """从百度获取静态地图，并缓存结果"""
    url = (
        f"http://api.map.baidu.com/staticimage/v2?"
        f"ak={BAIDU_AK}&center={lon},{lat}&zoom={zoom}&width={width}&height={height}"
    )
    resp = requests.get(url)
    return resp.content, resp.headers.get("Content-Type", "image/jpeg")

@app.route("/map")
def get_map():
    lon = request.args.get("lon")
    lat = request.args.get("lat")
    zoom = request.args.get("zoom", "13")
    width = request.args.get("width", "800")
    height = request.args.get("height", "600")

    if not (lon and lat):
        return {"error": "参数缺失：需要 lon, lat"}, 400

    try:
        img_data, content_type = fetch_baidu_map(lon, lat, zoom, width, height)
        return Response(img_data, mimetype=content_type)
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def index():
    return {"status": "ok", "usage": "/map?lon=103.09&lat=30.48"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
