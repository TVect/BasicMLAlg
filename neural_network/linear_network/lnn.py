# -*- coding:utf-8 -*-

'''
LMS for Linear Network
'''

import numpy as np

class LinearNetwork(object):

    def __init__(self):
        self.weights = None
        self.bias = None


    def training_lms(self, in_data, label, iter_num=100, eta=0.1, atol=1e-1):
        '''
        @param in_data: 训练数据
        @param label: 训练数据相应的标签
        '''
        in_arr = np.array(in_data)
        dim = in_arr.shape[1]
        self.bias = 0
        self.weights = np.random.rand(dim)

        for iter_i in xrange(iter_num):
            print("------------------- iter: %s -------------------" % iter_i)
            print "weights =", self.weights, self.bias
            print "error = ", np.dot(self.weights, in_data.T) + self.bias - label

            if np.allclose(np.dot(self.weights, in_data.T) + self.bias, label, atol=atol):
                break

            for in_id, in_item in enumerate(in_data):
                delta = label[in_id] - (np.dot(self.weights, in_item) + self.bias)
                if delta:
                    self.weights +=  delta * eta * in_item
                    self.bias += delta * eta


    def inference(self, test_data):
        return np.sign(np.dot(self.weights, test_data.T) + self.bias)
