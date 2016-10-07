# -*- coding: utf-8 -*-

import jieba
import re
import codecs
import numpy as np

def main():
    filename = "data/01.txt"
    pattern = re.compile(u'[。!　，]')

    with codecs.open("stopwords.txt", encoding="utf-8") as fr:
        stopwords = fr.read().split()

    with codecs.open(filename, encoding="utf-8") as fr:
        title = fr.readline().strip()
        text = []
        raw_text = []
        for line in fr:
            sents = pattern.split(line)
            for sent in sents:
                if sent.strip():
                    wds = [wd for wd in jieba.cut(sent.strip()) if wd not in stopwords]
                    if len(wds) > 2:
                        text.append(wds)
                        raw_text.append(sent.strip())

    # 构造权值矩阵W
    weights = np.zeros((len(text), len(text)))
    for i in range(len(text)):
        for j in range(i, len(text)):
            weights[i, j] = len(set(text[i]) & set(text[j])) / np.log(len(text[i]) * len(text[j]))
            weights[j, i] = weights[i, j]

        # 按行归一化
        line_sum = sum(weights[i,:])
        for j in range(len(text)):
            weights[i, j] /= line_sum

    d = 0.85
    weights = weights*d + 1.0*(1-d)/len(text)
    print weights

    iter = 100
    score = np.ones(len(text)) * 1.0/len(text)
    for it in xrange(iter):
#         new_score = np.dot(score, weights) * d + (1 - d)
        new_score = np.dot(score, weights)
        print np.sum((new_score-score)**2)
        score = new_score
    ret_dict = dict(zip(range(len(text)), score))
    sorted_items = sorted(ret_dict.iteritems(), key=lambda item: item[1], reverse=True)
    for id, value in sorted_items[:10]:
        print value
        print raw_text[id]

if __name__ == "__main__":
    main()
