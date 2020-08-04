"""Define the logistics to get data and construct web page
region_str_filter, extract_cities

Before 'city_name_transfer',
get_province_lock_map:
prov_lock_map:
get_china_lock_map:
lock_map:
"""

import json
import pickle
import random
import re
import requests
import os
import sys
from pyecharts.charts import Map, Timeline, Page
from pyecharts import options as opts
from pyecharts.options import MapItem
from pypinyin import lazy_pinyin
sys.path.append('.')
from config import LOCK_CONDITION_PATH, PROCESSED_JSON_PATH
test_path = os.getcwd()


def region_str_filter(string: str, words: list = ("省", "市", "自治区", "维吾尔", "回族", "壮族")):
    """
    remove postfix of regions
    :param string: target string
    :param words: keywords to remove
    :return:
    """
    for word in words:
        string = string.replace(word, "")
    return string


def extract_cities(prov_name):
    """
    extract relative cities for province
    :param prov_name
    :return:
    """
    prov_name_py = "".join(lazy_pinyin(prov_name))
    p = re.compile(r'name:"(.*?)"')
    res = requests.get('https://assets.pyecharts.org/assets/maps/{}.js'.format(prov_name_py))
    assert res.status_code == 200, 'Wrong pattern of province name'
    m = p.findall(res.text)
    return m


def city_name_transfer(prov_name, city_name: str):
    """
    Transfer the city name to the standardized one
    if not,
    :param prov_name: province
    :param city_name: target city
    :return:
    """
    cities = extract_cities(region_str_filter(prov_name))
    for cn in cities:
        if len(set(list(city_name)) & set(list(cn))) >= len(city_name) and city_name in cn:
            return cn
    print("no match, ", city_name)
    return city_name


def prov_lock_map(name, datapair):
    """
    Display province lock condition
    :param name:
    :param datapair:
    :return:
    """
    # if name == "china":
    #     n = "中国"
    # else:
    #     n = name
    # if name == "海南":
    #     center = [109.3, 19.10]
    #     zoom = 6
    # else:
    #     center = None
    #     zoom = 1
    print(datapair)
    prov_map = (
        Map().add(
            "lock down condition",
            data_pair=datapair,
            maptype=name,
            center=None,
            zoom=1).set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                      .set_global_opts(title_opts=opts.TitleOpts(title="{} lock condition".format(name)),
                                       visualmap_opts=opts.VisualMapOpts(split_number=4, is_piecewise=True,
                                                                         pieces=[{"min": 0, "max": 0,
                                                                                  "label": "unk", "color": "gray"},
                                                                                 {"min": 1, "max": 1,
                                                                                  "label": "close", "color": "yellow"},
                                                                                 {"min": 2, "max": 2,
                                                                                  "label": "semi-close", "color": "red"},
                                                                                 {"min": 3, "max": 3,
                                                                                  "label": "open", "color": "green"},
                                                                                 ]),
                                       legend_opts=opts.LegendOpts(is_show=False))
    )
    page = Page().add(prov_map).render_embed()
    return page


def get_province_lock_map(prov, time_index):
    """
    Get lock condition of a province at certain time point
    :param prov:
    :param time_index:
    :return: {city:{close/open}}
    """
    lock_map_data = []
    with open('%s/summary.pk' % LOCK_CONDITION_PATH, 'rb') as f:

        province_lock_summary = pickle.load(f)['province']
        time_series = sorted(list(province_lock_summary.keys()))
        assert len(time_series) > 0 or time_index < len(time_series), "Time index out of range"
        time_point = time_series[time_index]
    assert prov in province_lock_summary[time_point], "Province not in summary"
    for c in province_lock_summary[time_point][prov]:
        lock_map_data += [[city_name_transfer(prov, c), province_lock_summary[time_point][prov][c][0]]]
    return lock_map_data


def get_china_lock_map(time_index, time_interval=15):
    """
    Get lock condition during a time interval for china.
    :return: {time: {province: close/open}}
    """
    lock_map_data = {}
    with open('%s/summary.pk' % LOCK_CONDITION_PATH, 'rb') as f:
        china_lock_summary = pickle.load(f)['china']
    series = sorted(list(china_lock_summary.keys()))
    "change the data to show on web page with an interval of 30 days "
    start_index = max(0, int(time_index-time_interval))
    end_index = min(len(series), int(time_index+time_interval+1))
    for t in series[start_index:end_index]:
        lock_map_data[t] = []
        for p in china_lock_summary[t]:
            lock_map_data[t].append(MapItem(name=p, value=china_lock_summary[t][p][0]))
    return lock_map_data, start_index, time_index-start_index


def lock_map(map_data):
    """
    Construct timelined Map
    :param map_data:
    :return: Timeline object
    """
    tl = Timeline()
    sorted_timestamp = sorted(list(map_data.keys()))
    for t in sorted_timestamp:
        map0 = (
            Map().add(
                "lock condition", [p for p in map_data[t]], maptype='china'
            ).set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(visualmap_opts=opts.VisualMapOpts(split_number=4, is_piecewise=True,
                                                                         pieces=[
                                                                                 {"min": 0, "max": 0,
                                                                                  "label": "unk", "color": "gray"},
                                                                                 {"min": 1, "max": 1,
                                                                                  "label": "danger", "color": "yellow"},
                                                                                 {"min": 2, "max": 2,
                                                                                  "label": "close", "color": "red"},
                                                                                 {"min": 3, "max": 3,
                                                                                  "label": "open", "color": "green"},
                                                                                 ]),
                                 legend_opts=opts.LegendOpts(is_show=False)
                                 )
        )
        tl.add(map0, t)
    return tl


def get_china_lock_news(time_index):
    """
    Get lock evidence for each province at certain time point
    :param time_index:
    :return: 'news': related mblog news
    date: published date for the news
    """
    china_lock_news = []
    with open('%s/summary.pk' % LOCK_CONDITION_PATH, 'rb') as f:
        china_lock_summary = pickle.load(f)['china']
        time_series = sorted(list(china_lock_summary.keys()))
        time_point = time_series[time_index]
    for prov in china_lock_summary[time_point]:
        if len(china_lock_summary[time_point][prov][1]) == 0:
            continue
        show_blog_f_id = random.sample(china_lock_summary[time_point][prov][1], 1)[0]
        with open('%s/%s/%s.json' % (PROCESSED_JSON_PATH, prov, show_blog_f_id)) as f:
            china_lock_news.append(json.load(f)['微博正文'])
    return {'news': china_lock_news, 'date': time_point}



