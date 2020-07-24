import csv
# remove duplicate
import os
import pickle
import weibo_search.utils.util as util
import json


with open("utils/regions.pk", 'rb') as f:
    regions = pickle.load(f)


mblog_texts = {}
mblog_ids = []
cities = []
# print(os.listdir("output_files/original_csv"))
keywords = ['公共卫生响应']
# keywords = os.listdir("output_files/original_csv")
# deal with csv

for kw in keywords:
    if not os.path.exists('output_files/original_csv/%s/%s.csv' % (kw, kw)):
        continue
    with open('output_files/original_csv/%s/%s.csv' % (kw, kw), encoding='utf-8-sig') as f:

        f_csv = csv.DictReader(f)
        for blog in f_csv:
            if 'id' not in blog:
                print(blog)
                break
            b_id = blog['id']

            if blog['id'] not in mblog_ids:
                mblog_ids.append(blog['id'])
            else:
                continue

            t = blog['发布时间'][0:10]
            for r in regions:
                pub_prov = None
                if blog['微博正文'].find(r) > 0:
                    pub_prov = util.find_last_level_region(r)
                if pub_prov:
                    if not os.path.exists('../data/%s' % pub_prov):
                        os.mkdir('../data/%s' % pub_prov)
                    if not os.path.exists('../data/%s/%s_%s_%s.json' % (pub_prov, t, r, b_id)):
                        with open('../data/%s/%s_%s_%s.json' % (pub_prov, t, r, b_id), 'w')as f:
                            json.dump({'微博正文': blog['微博正文']}, f, ensure_ascii=False)







# f            if t not in mblog_texts:
#                 mblog_texts[t] = {}
#             for r in regions:
#                 if blog['微博正文'].find(r) > 0:
#                     pub_prov = util.find_last_level_region(r)
#
#                     if pub_prov not in mblog_texts[t]:
#                         mblog_texts[t][pub_prov] = []
#
#                     mblog_texts[t][pub_prov].append(blog['微博正文'])
print(len(mblog_ids))

# with open("output_files/weibo_data.json", 'w') as f:
#     json.dump(mblog_texts, f)
# json_paths = os.listdir("output_files/original_json_tweets")
# for json_path in json_paths:
#     with open(json_path) as f:
#          blog = json.load(f)






