"""Interface for client requests"""
import os
from flask import Flask, render_template, request, jsonify
from datetime import timedelta
from logistic import predict_china_lock_from_text, lock_map, predcit_province_lock_from_text, prov_lock_map, get_china_lock_news,get_province_lock_map,get_china_lock_map
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route("/")
def index():
    print("index")
    return render_template("index.html")


@app.route('/loading.gif')
def gif():
    with open('loading.gif', 'rb')as f:
         gif = f.read()
    print("loading")
    return gif


def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


@app.route("/map", methods=["GET", "POST"])
def get_map():
    data = request_parse(request)
    if 'start_time' in data:
        start_time = data['start_time']
    else:
        start_time = '2020-01-15'
    print("map start")
    # map_data = predict_china_lock_from_text(start_time=start_time, time_interval=70)
    map_data = get_china_lock_map()
    print("get data")
    return lock_map(map_data).dump_options_with_quotes()


@app.route("/pmap", methods=["GET", "POST"])
def get_pmap():
    data = request_parse(request)
    prov_name = data['prov_name']
    time_index = int(data['time_index'])
    # prov_map_data = predcit_province_lock_from_text(prov_name, time_index)
    prov_map_data = get_province_lock_map(prov_name, time_index)
    return prov_lock_map(prov_name, prov_map_data)


@app.route("/news", methods=["GET", "POST"])
def get_china_news():
    data = request_parse(request)
    time_index = int(data['time_index'])
    return jsonify(get_china_lock_news(time_index))


if __name__ == "__main__":
    # print(os.listdir('../data'))
    print(app.root_path)
    print(app.instance_path)
    print(os.path.dirname(app.instance_path))
    app.run(debug=True)

