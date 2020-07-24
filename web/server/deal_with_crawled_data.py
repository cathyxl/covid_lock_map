import csv
import os
import pickle
import weibo_search.utils.util as util
import json


def predict_lock_from_text(text):
    """
    Predict lock condition from a mblog text
    :param text:
    :return: lock: 1/2/3, score: corresponding score for each class
    """
    # todo: simple keyword match, need more refine


    lock = None
    keywords = {1: ['减缓', '无新增', '上调至二级', '下调至二级', '调至二级', '调到二级', '调整为二级', '升为二级'],
                2: ['封锁', '居家隔离', '减少聚集', '启动一级', '上调至一级', '调到一级', '调至一级', '升为一级'],
                3: ['解封', '复工', '放开通行', '下调至三级','下调为三级', '调至三级', '调到三级', '调整为三级']}

    for ind in keywords:
        for kw in keywords[ind]:
            if text.find(kw) > 0:
                lock = ind

    return lock, 0.0


def predict_lock_for_region(lock_list):
    """
    Combine all lock prediction results to get the final result
    Here we just choose the lock class with the maximum amount
    :param lock_list:
    :return: lock class, relative weibo file ids
    """
    lock_count = {1: 0, 2: 0, 3: 0}
    for lock in lock_list:
        if lock[1]:
            lock_count[lock[1]] += 1
    pred_lock = sorted(lock_count.items(), key=lambda k: k[1])[-1]

    rel_ids = []
    for lock in lock_list:
        if lock[1] == pred_lock[0]:
            rel_ids.append(lock[0])
    return pred_lock[0], rel_ids


def transfer_data_lock(crawled_data_files):
    """
    * Transfer crawled data to json files and save the predicted lock conditions into files.
    * Since this project did not implement database functions, this kind of saving methods could facilitate the future
    display on the website.
    * This code could deal with newly added crawled data by adding the new into the old saving system without affecting
    the old files, which could further be implemented as online crawlers.
    :param crawled_data_files:
    :return:
    """
    data_path = '../../data'
    mblogs = {}

    if not os.path.exists('%s/processed_data/mblog_ids.json' % data_path):
        mblog_ids = []
    else:
        with open('%s/processed_data/mblog_ids.json' % data_path) as f:
            mblog_ids = json.load(f)

    with open("../../weibo_search/utils/regions.pk", 'rb') as f:
        regions = pickle.load(f)
    for file_name in crawled_data_files:
        if not os.path.exists(file_name):
            continue
        with open(file_name, encoding='utf-8-sig') as f:
            f_csv = csv.DictReader(f)
            for blog in f_csv:
                b_id = blog['id']
                if b_id in mblog_ids:
                    continue
                else:
                    mblog_ids.append(b_id)
                t = blog['发布时间'][0:10]
                for r in regions:
                    # pub_prov = None
                    if blog['微博正文'].find(r) > 0:
                        p = util.find_last_level_region(r)
                    else:
                        continue
                    if p:
                        if t not in mblogs:  # time
                            mblogs[t] = {}
                        if p not in mblogs[t]:  # province
                            mblogs[t][p] = {}
                        if r not in mblogs[t][p]:  # city or province
                            mblogs[t][p][r] = []
                        b_f_id = '%s_%s_%s' % (t, r, b_id)
                        lock, score = predict_lock_from_text(blog['微博正文'])
                        mblogs[t][p][r].append([b_f_id, lock, score])
                        "write blog to file"
                        if not os.path.exists('%s/processed_data/%s' % (data_path, p)):
                            os.mkdir('%s/processed_data/%s' % (data_path, p))
                        if os.path.exists('%s/processed_data/%s/%s.json' % (data_path, p, b_f_id)):
                            continue
                        with open('%s/processed_data/%s/%s.json' % (data_path,p, b_f_id), 'w') as f:
                            json.dump({'微博正文': blog['微博正文'].replace('\n', ' ')}, f, ensure_ascii=False)

    with open('%s/processed_data/mblog_ids.json' % data_path, 'w') as f:
        json.dump(mblog_ids, f)
        print("write new mblog_ids")

    if not os.path.exists('%s/lock_condition/summary.pk' % data_path):
        china_lock_map_data = {}
        prov_lock_map_data = {}
    else:
        with open('%s/lock_condition/summary.pk' % data_path, 'rb') as f:
            a = pickle.load(f)
            china_lock_map_data = a['china']
            prov_lock_map_data = a['province']

    for t in mblogs:
        if t not in china_lock_map_data:
            china_lock_map_data[t] = {}
        if t not in prov_lock_map_data:
            prov_lock_map_data[t] = {}

        for p in mblogs[t]:
            if not os.path.exists('%s/lock_condition/%s' % (data_path, p)):
                os.mkdir('%s/lock_condition/%s' % (data_path, p))
            if p not in china_lock_map_data[t]:
                china_lock_map_data[t][p] = None
            if p not in prov_lock_map_data[t]:
                prov_lock_map_data[t][p] = {}

            new_prov_lock = []
            old_prov_lock = []
            for r in mblogs[t][p]:
                if r not in prov_lock_map_data[t][p]:
                    prov_lock_map_data[t][p][r] = None
                new_region_lock = []
                for item in mblogs[t][p][r]:
                    new_region_lock.append(item)

                new_prov_lock += new_region_lock
                if not os.path.exists('%s/lock_condition/%s/%s_%s.json' % (data_path, p, t, r)):
                    old_region_lock = []
                else:
                    with open('%s/lock_condition/%s/%s_%s.json' % (data_path, p, t, r)) as f:
                        old_region_lock = json.load(f)

                old_prov_lock += old_region_lock
                with open('%s/lock_condition/%s/%s_%s.json' % (data_path, p, t, r), 'w') as f:
                    print('dump new lock %s/%s_%s.json' % (p, t, r))
                    json.dump(old_region_lock + new_region_lock, f)

                prov_lock_map_data[t][p][r] = predict_lock_for_region(old_region_lock + new_region_lock)
            china_lock_map_data[t][p] = predict_lock_for_region(old_prov_lock + new_prov_lock)

    with open('%s/lock_condition/summary.pk' % data_path, 'wb') as f:
        a = {'china': china_lock_map_data, 'province': prov_lock_map_data}
        pickle.dump(a, f)
        print("write new summary")


if __name__ == '__main__':
    data_path = '../../weibo_search/output_files/original_csv'
    keywords = os.listdir(data_path)
    print(keywords)
    # keywords = ['全面复工']
    crawled_files = []
    # exit()
    for kw in keywords:
        if kw.startswith('.'):
            continue
        print('transfer  %s/%s/%s.csv' % (data_path, kw, kw))
        transfer_data_lock(['%s/%s/%s.csv' % (data_path, kw, kw)])
        # crawled_files.append('%s/%s/%s.csv' % (data_path, kw, kw))
    # print(crawled_files)
    # transfer_data_lock(crawled_files)


