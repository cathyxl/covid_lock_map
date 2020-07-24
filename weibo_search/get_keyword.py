import os
import csv
import jieba
# keywords = ['全面复工', '劝返点', '复工', '居家隔离', '解封', '返工']
keywords = ['公共卫生响应']
corpus = []
with open('../web/server/hit_stopwords.txt') as f:
    stopwords = f.read().splitlines()
for kw in keywords:
    with open('output_files/original_csv/%s/%s.csv' % (kw, kw)) as f:
        f_csv = csv.DictReader(f)
        for blog in f_csv:
            words = jieba.cut(blog['微博正文'])
            corpus.append(' '.join(words))
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

tf_vectorizer = CountVectorizer(stop_words=stopwords)
cntTf = tf_vectorizer.fit_transform(corpus)
lda = LatentDirichletAllocation(n_components=2,
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

n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)



