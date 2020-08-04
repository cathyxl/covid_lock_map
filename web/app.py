"""Interface for client requests"""
import os
from flask import Flask, render_template, request, jsonify
from datetime import timedelta
import json
from web.logistic import lock_map, prov_lock_map, get_china_lock_news, get_province_lock_map, get_china_lock_map


def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

    @app.route("/")
    def index():
        print("index")
        return render_template("index.html")

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route('/loading.gif')
    def gif():
        with open('loading.gif', 'rb')as f:
            gif = f.read()
        print("loading")
        return gif

    @app.route("/map", methods=["GET", "POST"])
    def get_map():
        """
        Get the lock map of whole China
        :return:
        lock_map: The lock map data to be shown on page
        st_ind: New start date on timeline
        ind: New index on timeline for the last clicked time point
        """
        data = request_parse(request)
        start_index = 0
        if 'start_index' in data:
            start_index = int(data['start_index'])
        time_index = int(data['time_index'])
        abs_time_index = start_index + time_index
        print(abs_time_index)

        print("map start")
        # map_data = predict_china_lock_from_text(start_time=start_time, time_interval=70)
        map_data, start_index, time_index = get_china_lock_map(abs_time_index)
        print("get data")
        str_map_options = lock_map(map_data).dump_options_with_quotes()
        a_object = json.loads(str_map_options)  # transfer str options into json object
        return jsonify({'lock_map': a_object, 'st_ind': start_index, 'ind': time_index})

    @app.route("/pmap", methods=["GET", "POST"])
    def get_pmap():
        """
        Get lock down condition for a province on certain date
        :return:
        """
        data = request_parse(request)
        prov_name = data['prov_name']
        "Get absolute time index in all data by adding start_index and the offset(time_index)"
        start_index = int(data['start_index'])
        time_index = int(data['time_index'])
        print(prov_name)
        abs_time_index = start_index + time_index
        # prov_map_data = predcit_province_lock_from_text(prov_name, time_index)
        print(abs_time_index)
        prov_map_data = get_province_lock_map(prov_name, abs_time_index)

        return prov_lock_map(prov_name, prov_map_data)

    @app.route("/news", methods=["GET", "POST"])
    def get_china_news():
        """Get mblog news in china that are related with the lock down condition for each province"""
        data = request_parse(request)
        start_index = int(data['start_index'])
        time_index = int(data['time_index'])
        abs_time_index = start_index + time_index
        return jsonify(get_china_lock_news(abs_time_index))
    # app.run()
    # app.add_url_rule("/", endpoint="index")
    return app


def request_parse(req_data):
    """
    Parse Request and get data
    :param req_data:
    :return:
    """
    if req_data.method == 'POST':
        data = req_data.json
    else:
        data = req_data.args
    return data


if __name__ == "__main__":
    app = create_app()
    print(app.root_path)
    print(app.instance_path)
    print(os.path.dirname(app.instance_path))
    app.run(debug=True)

# app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
#
#
# @app.route("/")
# def index():
#     print("index")
#     return render_template("index.html")
#
#
# @app.route('/loading.gif')
# def gif():
#     with open('loading.gif', 'rb')as f:
#          gif = f.read()
#     print("loading")
#     return gif
#
#

#
#
# @app.route("/map", methods=["GET", "POST"])
# def get_map():
#     """
#     Get the lock map of whole China
#     :return:
#     lock_map: The lock map data to be shown on page
#     st_ind: New start date on timeline
#     ind: New index on timeline for the last clicked time point
#     """
#     data = request_parse(request)
#     start_index = 0
#     if 'start_index' in data:
#         start_index = int(data['start_index'])
#     time_index = int(data['time_index'])
#     abs_time_index = start_index+time_index
#
#     print("map start")
#     # map_data = predict_china_lock_from_text(start_time=start_time, time_interval=70)
#     map_data, start_index, time_index = get_china_lock_map(abs_time_index)
#     print("get data")
#     str_map_options = lock_map(map_data).dump_options_with_quotes()
#     a_object = json.loads(str_map_options)  # transfer str options into json object
#     return jsonify({'lock_map': a_object, 'st_ind': start_index, 'ind': time_index})
#
#
# @app.route("/pmap", methods=["GET", "POST"])
# def get_pmap():
#     """
#     Get lock down condition for a province on certain date
#     :return:
#     """
#     data = request_parse(request)
#     prov_name = data['prov_name']
#     "Get absolute time index in all data by adding start_index and the offset(time_index)"
#     start_index = int(data['start_index'])
#     time_index = int(data['time_index'])
#     abs_time_index = start_index+time_index
#     # prov_map_data = predcit_province_lock_from_text(prov_name, time_index)
#     prov_map_data = get_province_lock_map(prov_name, abs_time_index)
#
#     return prov_lock_map(prov_name, prov_map_data)
#
#
# @app.route("/news", methods=["GET", "POST"])
# def get_china_news():
#     """Get mblog news in china that are related with the lock down condition for each province"""
#     data = request_parse(request)
#     start_index = int(data['start_index'])
#     time_index = int(data['time_index'])
#     abs_time_index = start_index + time_index
#     return jsonify(get_china_lock_news(abs_time_index))
#
#
# if __name__ == "__main__":
#     # print(os.listdir('../data'))
#     print(app.root_path)
#     print(app.instance_path)
#     print(os.path.dirname(app.instance_path))
#     app.run(debug=True)
#
