from pyecharts import options as opts
from pyecharts.charts import Map, Timeline
from pyecharts.faker import Faker
import os
import json
import jieba
corpus = []
corpus_times = []
with open('server/hit_stopwords.txt') as f:
    stopwords = f.read().splitlines()
data_path = '../data/安徽'
for file in os.listdir(data_path):
    with open('%s/%s' % (data_path, file)) as f:
        corpus_times.append(file[0:10])
        words = jieba.cut(json.load(f)['微博正文'])
        corpus.append(' '.join(words))

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

tf_vectorizer = CountVectorizer(stop_words=stopwords)
cntTf = tf_vectorizer.fit_transform(corpus)
lda = LatentDirichletAllocation(n_components=3,
                                max_iter=50,
                                learning_method='batch')
docres = lda.fit(cntTf)

def print_top_words(model, feature_names, n_top_words):
    #打印每个主题下权重较高的term
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

    print(model.components_)

n_top_words = 10
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)