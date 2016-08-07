# -*- coding: utf-8 -*-

'''
perceptron training algorithm
单个神经元的情形
'''

import numpy as np

class Perceptron(object):

    def __init__(self):
        self.weights = None
        self.bias = None


    def training_alg(self, in_data, label, iter_num=100, eta=1):
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
            print self.weights
            print self.bias
            if (label == np.sign(np.dot(self.weights, in_data.T) + self.bias)).all():
                break

            for in_id, in_item in enumerate(in_data):
                delta = label[in_id] - np.sign(np.dot(self.weights, in_item) + self.bias)
                if delta:
                    self.weights +=  delta * eta * in_item
                    self.bias += delta * eta


    def inference(self, test_data):
        return np.sign(np.dot(self.weights, test_data.T) + self.bias)
