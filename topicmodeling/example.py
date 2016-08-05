# -*- coding: utf-8 -*-

'''
Created on 2016-7-25

@author: chin
'''

from plsa.plsa import PLSA
from lda.lda import LDA
import re
import os
import pickle

import sys
reload(sys)
sys.setdefaultencoding("utf8")


word_list = []
word_dict = {}
docs = []


def prepare_data_from_dir(train_dir, stopword_set):
    non_chinese = re.compile(u"[^\u4E00-\u9FA5]")   # 所有非汉字的unicode编码范围
    for filename in os.listdir(train_dir):
        with open(os.path.join(train_dir, filename)) as fr:
            print filename
            doc = []
            words = non_chinese.sub(" ", fr.read().decode("utf-8"))
            for word in words.strip().split():
                if word in stopword_set:
#                     print word
                    continue
                if word not in word_list:
                    word_dict[word] = len(word_list)
                    word_list.append(word)
                doc.append(word_dict[word])
            docs.append(doc)


def filter_stopwords(filename):
    stopword_set = set([])
    with open(filename) as fr:
        for word in fr:
            stopword_set.add(word.strip().decode("utf-8"))
    return stopword_set


def result_save(plsa_method, result_path="result/new"):
    with open(os.path.join(result_path, "doc_topic.txt"), "w") as fw:
        for row in plsa_method.pdoc_topic:
            for prob in row:
                fw.write("%f\t" % prob)
            fw.write("\n")
    with open(os.path.join(result_path, "topic_word.txt"), "w") as fw:
        for row_id, row in enumerate(plsa_method.ptopic_word):
            fw.write("class: %d\n" % row_id)
            topic_word_prob = dict(zip(word_list, row))
            for word, prob in sorted(topic_word_prob.iteritems(), key=lambda item: item[1], reverse=True)[:20]:
                fw.write(u"\t%s\t%f\n" % (word, prob))
            fw.write(os.linesep)


def test_plsa():
    plsa_method = PLSA(docs=docs)
    plsa_method.training_em(topic_num=3, iter_num=100, epsilon=1e-6)
    result_save(plsa_method)


def test_lda():
    lda_method = LDA(docs=docs)
    lda_method.gibbs_sampling(topic_num=3, iter_num=100, epsilon=1e-6)
    result_save(lda_method)


def main_test():
#     prepare_data_from_dir(u"E:\\07-Repository\\语料\\data-分类", filter_stopwords("stopwords.txt"))
#     pickle.dump(docs, file("result/new/docs.list", "w"))
#     pickle.dump(word_list, file("result/new/words.list", "w"))
    global docs
    global word_list
    docs = pickle.load(file("result/new/docs.list"))
    word_list = pickle.load(file("result/new/words.list"))

#     test_lda()
    test_plsa()    


if __name__ == "__main__":
    main_test()
