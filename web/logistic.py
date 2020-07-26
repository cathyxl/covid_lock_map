"""Define the logistics to get data and construct web page"""
import json
import pickle
import random
import re
import requests
import os
from pyecharts.charts import Map, Timeline, Page
from pyecharts import options as opts
from datetime import datetime, timedelta

from pyecharts.options import MapItem
from pypinyin import lazy_pinyin
from deal_with_crawled_data import predict_lock_from_text, predict_lock_for_region


test_path = os.getcwd()

def str_filter(string: str, words: list = ("省", "市", "自治区", "维吾尔", "回族", "壮族")):
    """
    remove postfix of regions
    :param string: target string
    :param words: keywords to remove
    :return:
    """
    for word in words:
        string = string.replace(word, "")
    return string


def extract(prov_name):
    """
    extract relative cities for province
    :param prov_name
    :return:
    """
    prov_name_py = "".join(lazy_pinyin(prov_name))
    p = re.compile(r'name:"(.*?)"')
    res = requests.get('https://assets.pyecharts.org/assets/maps/{}.js'.format(prov_name_py))
    m = p.findall(res.text)
    return m


def city_name_transfer(prov_name, city_name: str):
    """
    :param prov_name: province
    :param city_name: target city
    :return:
    """
    cities = extract(prov_name)
    for cn in cities:
        if len(set(list(city_name)) & set(list(cn))) >= len(city_name) or city_name in cn:
            return cn
    print("no", city_name)
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


def get_china_lock_map(time_index, time_interval=15):
    """
    Get lock condition during a time interval for china.
    :return: {time: {province: close/open}}
    """
    lock_map_data = {}
    with open('../data/lock_condition/summary.pk', 'rb') as f:
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


def get_province_lock_map(prov, time_index):
    """
    Get lock condition of a province at certain time point
    :param prov:
    :param time_index:
    :return: {city:{close/open}}
    """
    lock_map_data = []
    with open('../data/lock_condition/summary.pk', 'rb') as f:
        province_lock_summary = pickle.load(f)['province']
        time_series = sorted(list(province_lock_summary.keys()))
        time_point = time_series[time_index]
    for c in province_lock_summary[time_point][prov]:
        lock_map_data += [[city_name_transfer(prov, c), province_lock_summary[time_point][prov][c][0]]]
    return lock_map_data


def get_china_lock_news(time_index):
    """
    Get lock evidence for each province at certain time point
    :param time_index:
    :return: 'news': related mblog news
    date: published date for the news
    """
    data_path = '../data/processed_data'
    china_lock_news = []
    with open('../data/lock_condition/summary.pk', 'rb') as f:
        china_lock_summary = pickle.load(f)['china']
        time_series = sorted(list(china_lock_summary.keys()))
        time_point = time_series[time_index]
    for prov in china_lock_summary[time_point]:
        if len(china_lock_summary[time_point][prov][1]) == 0:
            continue
        show_blog_f_id = random.sample(china_lock_summary[time_point][prov][1], 1)[0]
        with open('%s/%s/%s.json' % (data_path, prov, show_blog_f_id)) as f:
            china_lock_news.append(json.load(f)['微博正文'])
    return {'news': china_lock_news, 'date': time_point}


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

"""This two method is used to predict lock down condition in realtime pattern.
Considering the time delay for computing, this two methods are deprecated. Now 
the lock down condition is computed before hand, right after crawled from website."""


def predcit_province_lock_from_text(prov_name, time_index=0):
    """
    Predict city lock for a province from data in realtime pattern,
    This method is kind of slow, so I just calculate lock down
    when dealing with initial crawled data.
    :param prov_name:
    :param time_index:
    :return:
    """
    data_path = '../data/processed_data'
    mblogs = {}
    mblog_texts = {}
    time_points = []
    for blog_file in os.listdir('%s/%s' % (data_path, prov_name)):
        if blog_file[0:10] not in time_points:
            time_points.append(blog_file[0:10])
    time_points = sorted(time_points)
    cur_time_point = time_points[time_index]

    for blog_file in os.listdir('%s/%s' % (data_path, prov_name)):
        if blog_file.startswith(cur_time_point):
            c = blog_file.split('_')[1]
            m_id = blog_file.split('_')[2][0:-5]
            with open('%s/%s/%s' % (data_path, prov_name, blog_file)) as f:
                blog_text = json.load(f)['微博正文']
                mblog_texts[m_id] = blog_text
                if c not in mblogs:
                    mblogs[c] = []
                mlock, score = predict_lock_from_text(blog_text)
                mblogs[c].append([mlock, m_id, score])
    prov_lock_data = []
    show_blog_texts = []
    for c in mblogs:
        lock, rel_ids = predict_lock_for_region(mblogs[c])
        show_m_id = random.sample(rel_ids, 1)
        show_blog_texts.append(mblog_texts[show_m_id])
        prov_lock_data += [[city_name_transfer(prov_name, c), lock]]
        # prov_lock_data.append(MapItem(name=c, value=lock))
    print(prov_lock_data)
    print(show_blog_texts)

    return prov_lock_data, show_blog_texts


def predict_china_lock_from_text(start_time='2020-03-15', time_interval=30):
    """
        Predict lock from data in realtime pattern,
        This method is kind of slow, so I just calculate lockdown
        when dealing with initial crawled data.
        :param start_time:
        :param time_interval:
        :return:
        """
    mblogs = {}
    mblog_texts = {}
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = start_time + timedelta(time_interval)
    data_path = '../data/processed_data'
    for prov in os.listdir(data_path):
        for blog_file in os.listdir('%s/%s' % (data_path, prov)):
            t = blog_file[0:10]
            m_id = blog_file.split('_')[2][0:-5]
            if start_time <= datetime.strptime(t, '%Y-%m-%d') < end_time:
                with open('%s/%s/%s' % (data_path, prov, blog_file)) as f:
                    blog_text = json.load(f)['微博正文']
                mblog_texts[m_id] = blog_text
                if t not in mblogs:
                    mblogs[t] = {}
                if prov not in mblogs[t]:
                    mblogs[t][prov] = []
                mlock, score = predict_lock_from_text(blog_text)
                mblogs[t][prov].append([mlock, m_id, score])

    china_map_lock = {}
    show_blog_texts = []
    for t in mblogs:
        if t not in china_map_lock:
            china_map_lock[t] = []

        for p in mblogs[t]:
            lock, rel_ids = predict_lock_for_region(mblogs[t][p])
            # lock = predict_lock_from_text(' '.join(mblogs[t][p]))
            show_m_id = random.sample(rel_ids, 1)
            show_blog_texts.append(mblog_texts[show_m_id.split('_')[-1]])
            china_map_lock[t].append(MapItem(name=p, value=lock))

            # china_map_lock[t] += [[p, lock]]
    return china_map_lock, show_blog_texts

# if __name__ == '__main__':
# print(lock_map())
