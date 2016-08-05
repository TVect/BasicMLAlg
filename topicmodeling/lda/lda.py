# -*- coding: utf-8 -*-

'''
Created on 2016-8-5

@author: chin
'''

import numpy as np

class LDA(object):
    '''
    cnt_m_k: document-topic count, i.e., the number of times that topic k has been observed with a word of documents m
    cnt_m: document-topic sum
    cnt_k_t: topic-term count, i.e., the number of times that term t has been observed with topic k
    cnt_k: topic-term sum
    '''

    alpha = 2.0
    beta = 2.0

    def __init__(self, docs):
        self.pdoc_topic = None
        self.ptopic_word = None

        self.word_set = []
#         self.docs = docs    # 需要每个doc是一个list而不是一个dict
        self.docs = [[[wd, -1] for wd in doc] for doc in docs]

        self._initial_wordset()


    def _initial_wordset(self):
        for doc in self.docs:
            for word in doc:
                self.word_set.append(word)


    def gibbs_sampling(self, topic_num=3, iter_num=100, epsilon=1e-6):
        '''
        @param topic_num: 主题个数
        @param iter_num: 迭代次数上限
        @param epsilon: 误差上限，当前后两次的Q函数值小于epsilon时会停止迭代
        '''
        # initialisation
        cnt_m = np.zeros(len(self.docs))
        cnt_m_k = np.zeros((len(self.docs), topic_num))
        cnt_k = np.zeros(topic_num)
        cnt_k_t = np.zeros((topic_num, len(self.word_set)))
        for doc_id, doc in enumerate(self.docs):
            for item in doc:
                # sample topic index z ~ Multi(1/topic_num)
                t_id = np.random.multinomial(1, [1.0/topic_num]*topic_num).argmax()
                cnt_m_k[doc_id][t_id] += 1
                cnt_m[doc_id] += 1
                cnt_k_t[t_id][item[0]] += 1
                cnt_k[t_id] += 1
                item[1] = t_id

        # Gibbs Sampling over burn-in period and sampling period
        for iter_i in xrange(iter_num):
            print("------------------------ iter: %s ------------------------" % iter_i)
            for doc_id, doc in enumerate(self.docs):
                for item in doc:
                    # for the current assignment of topic k to a term t for word w, decrease counts and sums
                    cnt_m_k[doc_id][item[1]] -= 1
                    cnt_m[doc_id] -= 1
                    cnt_k_t[item[1]][item[0]] -= 1
                    cnt_k[item[1]] -= 1

                    # multinomial sampling acc. to p(zi | z-i, w)
                    full_cond = []
                    for t_id in xrange(topic_num):
                        if t_id == item[1]:
                            full_cond.append((cnt_k_t[t_id][item[0]] -1 + self.beta) * 
                                             (cnt_m_k[doc_id][t_id] + self.alpha) / 
                                             (np.sum([cnt_k_t[t_id][wd] for wd in self.word_set]) + self.beta - 1))
                        else:
                            full_cond.append((cnt_k_t[t_id][item[0]] + self.beta) * 
                                             (cnt_m_k[doc_id][t_id] + self.alpha) / 
                                             (np.sum([cnt_k_t[t_id][wd] for wd in self.word_set]) + self.beta - 1))
                    full_cond = np.array(full_cond) / np.sum(full_cond)
#                     print full_cond
                    # use the new assignment of topic k to a term t for word w, increase counts and sums
                    t_id = np.random.multinomial(1, full_cond).argmax()
                    cnt_m_k[doc_id][t_id] += 1
                    cnt_m[doc_id] += 1
                    cnt_k_t[t_id][item[0]] += 1
                    cnt_k[t_id] += 1
                    item[1] = t_id

            # check convergence and read out parameters
            pass

        # read out parameters
        self.ptopic_word = ((cnt_k_t + self.beta).T / (np.sum(cnt_k_t, axis=1) + self.beta)).T
        self.pdoc_topic = ((cnt_m_k + self.alpha).T / (np.sum(cnt_m_k, axis=1) + self.alpha)).T
        