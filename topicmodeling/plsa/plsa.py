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
    
    def __init__(self, docs):
        '''
        @param docs: list of list
        '''
        self.pdoc_topic = None
        self.ptopic_word = None

        self.word_set = set([])
        self.docs = []
        for doc in docs:
            doc_dict = {}
            for wd in doc:
                self.word_set.add(wd)
                doc_dict.setdefault(wd, 0)
                doc_dict[wd] += 1
            self.docs.append(doc_dict)


    def training_em(self, topic_num=3, iter_num=100, epsilon=1e-6, train_data="data/train.dat"):
        '''
        @param topic_num: 主题个数
        @param iter_num: 迭代次数上限
        @param epsilon: 误差上限，当前后两次的Q函数值小于epsilon时会停止迭代
        @param train_data: 训练数据的位置
        '''
#         self.topic_num = topic_num
#         self.prepare_data(train_data)
#         self.prepare_data_from_dir(train_data)
        self.random_initial_probabity(topic_num)
        
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
                    for topic_id in xrange(topic_num):
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


    def random_initial_probabity(self, topic_num):
        self.pdoc_topic = preprocessing.normalize(np.random.random((len(self.docs), topic_num)), norm="l1", axis=1)
        self.ptopic_word = preprocessing.normalize(np.random.random((topic_num, len(self.word_set))), norm="l1", axis=1)        

