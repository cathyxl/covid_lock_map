import json

import jieba.analyse
import matplotlib as mpl
from scipy.misc import imread
from wordcloud import WordCloud
import csv
import pandas as pd
# mpl.use('TkAgg')
import matplotlib.pyplot as plt
import weibo_search.utils.util as util

def keywords(mblogs):
    text = []
    for blog in mblogs:
        keyword = jieba.analyse.extract_tags(blog['text'])
        text.extend(keyword)
    return text


def gen_img(texts, img_file):
    data = ' '.join(text for text in texts)
    image_coloring = imread(img_file)
    wc = WordCloud(
        background_color='white',
        mask=image_coloring,
        font_path='/Library/Fonts/STHeiti Light.ttc'
    )
    wc.generate(data)

    # plt.figure()
    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()

    wc.to_file(img_file.split('.')[0] + '_wc.png')


if __name__ == '__main__':
    keyword = '新冠肺炎'
    words = []
    times = []
    locs = []
    loc_freq = {}

    for prov in util.region_dict:
        if prov not in locs:
            locs.append(prov)
            loc_freq[prov] = {}
        for c in util.region_dict[prov]['city']:
            locs.append(c)
            loc_freq[c] = {}
    # print(locs)
    # exit()


    # print(locs)
    # exit()

    p = 0
    n = 0
    with open('output_files/%s/%s.csv' % (keyword, keyword)) as f:
        f_csv = csv.DictReader(f)

        for blog in f_csv:
            n += 1
            flag = 0
            for loc in locs:

                t = blog['发布时间'][0:10]
                if blog['微博正文'].find(loc) > 0:
                    flag = 1
                    if t not in loc_freq[loc]:
                        loc_freq[loc][t] = 0
                    loc_freq[loc][t] += 1
            p += flag
            # t = blog['微博正文']

            # if t not in times:
            #     times.append(t)
    print(p, n, float(p/n))
    print(loc_freq)

    # print(sorted(loc_freq.items(), key=lambda k:k[1]))


    # print(sorted(times))

            # words.extend(jieba.analyse.extract_tags(blog['微博正文']))
    # words = []
    # # for row in f_csv:
    #
    #
    # mblogs = json.loads(open('result_{}.json'.format(keyword), 'r', encoding='utf-8').read())
    # print('微博总数：', len(mblogs))
    #
    # words = []
    # for blog in mblogs:
    #     words.extend(jieba.analyse.extract_tags(blog['text']))
    #
    # print("总词数：", len(words))
    #
    # gen_img(words, 'edge.png')

