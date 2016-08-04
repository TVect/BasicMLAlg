# -*- coding: utf-8 -*-

'''
Created on 2016-8-4

@author: chin
'''

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from em_gmm import EM_GMM

def test_uni():
    s1 = np.random.normal(0, np.sqrt(1.5), 1000)
    s2 = np.random.normal(5, np.sqrt(1.5), 1000)
    s = np.where(np.random.random(1000) > 0.5, s1, s2)
    in_arr = np.matrix(s).T
    
    gmm_method = EM_GMM()
    gmm_method.mainframe(in_arr, cluster_cnt=2, iter_limit=100)


# s = np.where(np.random.random(10000) > 0.5, s1, s2)
# 
# count, bins, ignored = plt.hist(s, 30, normed=True)
# 
# plt.plot(bins, stats.norm.pdf(bins, loc=0, scale=1.5), 'r-')
# plt.plot(bins, stats.norm.pdf(bins, loc=5, scale=1.5), 'r-')
# 
# plt.show()


# TODO 多维正态分布函数
def test_multi():
    pass


if __name__ == "__main__":
    test_uni()