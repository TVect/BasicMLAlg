# -*- coding: utf-8 -*-

'''
Created on 2016-7-21

@author: chin
'''

import os
import numpy as np
from sklearn import preprocessing
import math

class PLSA(object):
    
    def __init__(self):
#         self.pdoc = None
        self.pdoc_topic = None
        self.ptopic_word = None

        self.word_dict = {}
        self.words = []
        self.docs = []


    def training_em(self, topic_num=3, iter_num=100, epsilon=1e-6, train_data="data/train.dat"):
        '''
        @param topic_num: 主题个数
        @param iter_num: 迭代次数上限
        @param epsilon: 误差上限，当前后两次的Q函数值小于epsilon时会停止迭代
        @param train_data: 训练数据的位置
        '''
        self.topic_num = topic_num
        self.prepare_data(train_data)
        self.random_initial_value()
        
        # 临时的p(topic|doc, word), 为了防止维护的临时矩阵过大，下面会对每一个doc轮流处理        
        old_Qvalue = 0.0
        new_Qvalue = 0.0
        for iter_i in xrange(iter_num):
            print "------------iter:", iter_i
            old_Qvalue = new_Qvalue
            new_Qvalue = 0.0
            tmp_ptopic_word = np.zeros(self.ptopic_word.shape)
            tmp_pdoc_topic = np.zeros(self.pdoc_topic.shape)
            for doc_id, doc in enumerate(self.docs):
                for wd_id, wd_cnt in doc.iteritems():
                    tmp_ptopic_given_docwd = self.pdoc_topic[doc_id] * self.ptopic_word[:, wd_id]
                    tmp_ptopic_given_docwd = tmp_ptopic_given_docwd / float(sum(tmp_ptopic_given_docwd))                        
                    for topic_id in xrange(self.topic_num):
                        tmp_pdoc_topic[doc_id][topic_id] += wd_cnt * tmp_ptopic_given_docwd[topic_id]
                        tmp_ptopic_word[topic_id][wd_id] += wd_cnt * tmp_ptopic_given_docwd[topic_id]

            self.pdoc_topic = preprocessing.normalize(tmp_pdoc_topic, norm="l1", axis=1)
            self.ptopic_word = preprocessing.normalize(tmp_ptopic_word, norm="l1", axis=1)
            
            for doc_id, doc in enumerate(self.docs):
                for wd_id, wd_cnt in doc.iteritems():
                    new_Qvalue -= math.log(sum(self.pdoc_topic[doc_id] * self.ptopic_word[:, wd_id])) * wd_cnt
            
            print new_Qvalue
            if abs(new_Qvalue - old_Qvalue) < (old_Qvalue * epsilon):
                break
#         print self.ptopic_word
#         print self.pdoc_topic


    def prepare_data(self, train_data):
        for line in file(train_data):
            doc = {}
            words = line.strip().split()
            for word in words:
                if word not in self.words:
                    self.word_dict[word] = len(self.words)
                    self.words.append(word)
                doc.setdefault(self.word_dict[word], 0)
                doc[self.word_dict[word]] += 1
            self.docs.append(doc)


    def random_initial_value(self):
        self.pdoc_topic = preprocessing.normalize(np.random.random((len(self.docs), self.topic_num)), norm="l1", axis=1)
        self.ptopic_word = preprocessing.normalize(np.random.random((self.topic_num, len(self.word_dict))), norm="l1", axis=1)


    def result_save(self, result_path):
        with open(os.path.join(result_path, "doc_topic.txt"), "w") as fw:
            for row in self.pdoc_topic:
                for prob in row:
                    fw.write("%f\t" % prob)
                fw.write("\n")
        with open(os.path.join(result_path, "topic_word.txt"), "w") as fw:
            for row_id, row in enumerate(self.ptopic_word):
                fw.write("class: %d\n" % row_id)
                topic_word_prob = dict(zip(self.words, row))
                for word, prob in sorted(topic_word_prob.iteritems(), key=lambda item: item[1], reverse=True)[:20]:
                    fw.write("\t%s\t%f\n" % (word, prob))
                fw.write(os.linesep)


if __name__ == "__main__":
    plsa_method = PLSA()
    plsa_method.training_em(topic_num=3, iter_num=100, train_data="data/train.dat")

#     plsa_method.result_save(result_path="data/")

    print len(plsa_method.words)
    print plsa_method.pdoc_topic