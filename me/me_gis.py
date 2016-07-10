# -*- coding:utf-8 -*-

u'''
ME solution -- GIS:
    P(A)+P(B)+P(C)+P(D)+P(E)=1
    P(A)+P(B)=3/10
    P(A)+P(C)=1/2
参考：《统计自然语言处理》 Page124 宗成庆

'''

import numpy as np


def feature_0(x):
    return 1

def feature_1(x):
    if x in [1,2]:
        return 1
    else:
        return 0

def feature_2(x):
    if x in [1,3]:
        return 1
    else:
        return 0

def max_constant(varis, features):
    max_const = max([sum([feature(x) for feature in features]) for x in varis])
    return max_const


def calc_probs(params, varis, features):
    '''
    计算最大熵
    @param params: features的系数
    @param varis: 随机变量的取值范围
    @param features: 特征函数
    '''
    feat_cnt = len(features)
    var_cnt = len(varis)
    probs = []
    for vari in varis:
        probs.append(np.exp(sum([params[j]*features[j](vari) for j in xrange(feat_cnt)])))
    probs = np.array(probs)/sum(probs)
    return probs
    expectations = [sum([probs[i] * feature(varis[i]) for i in xrange(var_cnt)]) for feature in features]
    return expectations
    

def gis_method(varis, features, constrains):
    '''
    @param varis: 随机变量可以取得值
    '''
    max_const = max_constant(varis, features)
#     print max_const
    correction_feature = lambda x: max_const - sum([feature(x) for feature in features])
    modified_features = list(features)
    modified_features.append(correction_feature)
    modified_contrains = list(constrains)
    modified_contrains.append(max_const - sum(constrains))
#     print modified_contrains
    params = np.array([0.0] * (len(modified_features)))
    
    for it in xrange(100):
        probs = calc_probs(params, varis, modified_features)
        print "probs:", probs
        expectations = [sum([probs[i] * feature(varis[i]) 
                             for i in xrange(len(varis))]) 
                        for feature in modified_features]
        print expectations
        params += [modified_contrains[i]/(expectations[i]*max_const) for i in xrange(len(modified_features))]


if __name__ == '__main__':
    gis_method([1,2,3,4,5], [feature_1, feature_2], [3.0/10, 1.0/2])
