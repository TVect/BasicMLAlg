# -*- coding:utf-8 -*-

u'''
CRF viterbi-alg: 用viterbi算法求解CRF的预测问题
Problem:
    参见：《统计学习方法》 李航 Page196 例11.1
Solution：
    参见：《统计学习方法》 李航 Page207 例11.3

'''

def feature_1(y, idx):
    if idx in [1,2]:
        if (y[idx-1] == 1) and (y[idx] == 2):
            return 1
    return 0

def feature_2(y, idx):
    if idx == 1:
        if (y[idx-1] == 1) and (y[idx] == 1):
            return 1
    return 0

def feature_3(y, idx):
    if idx == 2:
        if (y[idx-1] == 2) and (y[idx] == 1):
            return 1
    return 0

def feature_4(y, idx):
    if idx == 1:
        if (y[idx-1] == 2) and (y[idx] == 1):
            return 1
    return 0

def feature_5(y, idx):
    if idx == 2:
        if (y[idx-1] == 2) and (y[idx] == 2):
            return 1
    return 0

def feature_6(y, idx):
    if idx == 0:
        if y[idx] == 1:
            return 1
    return 0

def feature_7(y, idx):
    if idx in [0, 1]:
        if y[idx] == 2:
            return 1
    return 0

def feature_8(y, idx):
    if idx in [1, 2]:
        if y[idx] == 1:
            return 1
    return 0

def feature_9(y, idx):
    if idx == 2:
        if y[idx] == 2:
            return 1
    return 0

def prob(y, features, params):
    ret = 0
    for idx_feat, feature in enumerate(features):
        for idx in range(len(y)):
            if feature(y, idx) != 0:
                ret += feature(y, idx) * params[idx_feat]
    return ret


def prob_idx(y, features, params, idx):
    '''
    对所有特征函数在指定位置的值进行求和
    '''
    return sum([feature(y, idx) * params[idx_feat] for idx_feat, feature in enumerate(features)])


def simple_viterbi(leng, y_range, features, params):
    best_paths = [[]] * len(y_range) # 记录到当前位置的最优路径
    best_probs = [0] * len(y_range) # 记录到当前位置的最优路径对应的概率
    for i in range(leng):
        tmp_probs = [[prob_idx(best_paths[k]+[y_value], features, params, i) + best_probs[k] 
         for k in range(len(y_range))] for j, y_value in enumerate(y_range)]
        best_probs = [max(tmp_prob) for tmp_prob in tmp_probs]
        best_paths = [best_paths[tmp_probs[i].index(best_prob)] + [y_range[i]] 
                      for i, best_prob in enumerate(best_probs)]

        print best_probs
    return best_paths[best_probs.index(max(best_probs))]

features = [feature_1, feature_2, feature_3, feature_4, feature_5, 
            feature_6, feature_7, feature_8, feature_9]
params = [1, 0.6, 1, 1, 0.2, 1, 0.5, 0.8, 0.5]

print simple_viterbi(leng=3, y_range=[1,2], features=features, params=params)