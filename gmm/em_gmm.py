# -*- coding: utf-8 -*-

'''
Created on 2016-8-4

@author: chin
'''

import numpy as np

def multi_guassin_pdf(x, mu=0, sigma=1):
    '''
    高维高斯密度函数
    '''
    val = -0.5 * (np.matrix(x)-np.matrix(mu)) * np.matrix(sigma).I * (np.matrix(x)-np.matrix(mu)).T
    return np.exp(val[0,0]) / (np.power((2*np.pi), np.matrix(mu).size/2.0) * np.power(np.linalg.det(np.matrix(sigma)), 0.5))


class EM_GMM(object):

    '''
    EM for Guassian Mixture Model
    '''

    def __init__(self):
        self.coef_list = []
        self.mu_list = []
        self.sigma_list = []
        self.cluster_cnt = None
        self.k_dim = 1


    def mainframe(self, in_arr, cluster_cnt, iter_limit=2):
        in_arr = np.array(in_arr)
        k_size, k_dim = in_arr.shape # 列表示是几纬的数据
        self.k_dim = k_dim
        self.cluster_cnt = cluster_cnt

        self.coef_list = np.random.random(self.cluster_cnt)
        self.coef_list = self.coef_list / self.coef_list.sum()

        self.sigma_list = [np.eye(self.k_dim, self.k_dim) for _ in range(cluster_cnt)]
        self.mu_list = [in_arr[int(i)] for i in np.linspace(0, k_size-1, num=cluster_cnt)]

        for it in range(iter_limit):
            print "------------------iter:", it
            print "mu:", self.mu_list
            print "sigma", self.sigma_list
            print "coef", self.coef_list

            gam_nk = [] #反映了数据 n属于类别 k的概率
            # e-step
            for in_samp in in_arr:
                gam = [multi_guassin_pdf(in_samp, self.mu_list[k], self.sigma_list[k]) 
                       * self.coef_list[k] for k in range(cluster_cnt)]
                gam_nk.append(np.array(gam) / float(np.sum(gam)))
            # m-step
            tmp_nk = np.sum(gam_nk, axis=0)
            self.coef_list = tmp_nk / k_size
#             print self.coef_list
            for k in range(self.cluster_cnt):
                u_sum = np.zeros(k_dim)
                sigma_sum = np.zeros((k_dim, k_dim))
                for i in range(k_size):
                    u_sum += gam_nk[i][k] * in_arr[i]
                self.mu_list[k] = u_sum / tmp_nk[k]
                for i in range(k_size):
                    sigma_sum += gam_nk[i][k] * np.mat(in_arr[i]-self.mu_list[k]).T * np.mat(in_arr[i]-self.mu_list[k])
                self.sigma_list[k] = sigma_sum / tmp_nk[k]

