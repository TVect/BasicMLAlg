# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

'''
Created on 2017年6月24日

@author: Chin
@summary: 周志华 机器学习 P303

'''

class LabelSpreading(object):
    
    def __init__(self):
        pass
    
    
    def process(self, labeled_df, unlabeled_df, sigma=1, alpha=0.5, iter=100):
        '''
        @param labeled_df: 有标注的df, 标注列名为class
        @param unlabeled_df: 无标注的df, 即无class列
        @param sigma: 构图参数
        @param alpha: 折中参数
        '''
        samples = pd.concat([labeled_df.iloc[:, :-1], unlabeled_df])
        # 亲和矩阵
        affinity_matrix = self.init_affinity_matrix(samples, sigma=1)
        d_matrix_sqrt = np.diag(1.0 / np.sqrt(np.sum(affinity_matrix, axis=0)))
        # 标记传播矩阵
        trans_matrix = d_matrix_sqrt.dot(affinity_matrix).dot(d_matrix_sqrt)
        labels = list(set(labeled_df["class"].values))
        # 矩阵Y
        y_matrix = np.zeros([samples.shape[0], len(labels)])
        
        for i in range(labeled_df.shape[0]):
            y_matrix[i][labels.index(labeled_df.iloc[i][-1])] = 1
        # print(y_matrix)
        
        # 标记矩阵更新
        old_f = y_matrix
        for j in xrange(iter):
            new_f = np.dot(trans_matrix, old_f) * alpha + y_matrix * (1 - alpha)
            old_f = new_f
        # print(new_f)
        
        # 根据标记矩阵确定label分配
        assigned_df = unlabeled_df.copy()
        assigned_class = new_f.argmax(axis=1)[labeled_df.shape[0]:]
        # print(assigned_class)
        # print(len(assigned_class))
        assigned_df["class"] = [labels[idx] for idx in assigned_class]
        # print(assigned_df)
        return assigned_df
        

    def init_affinity_matrix(self, samples, sigma):
        '''
        @summary: 初始化亲和矩阵
        '''
        sample_cnts = samples.shape[0]
        affinity_matrix = np.zeros([sample_cnts, sample_cnts])
        for i in range(sample_cnts):
            for j in range(i+1, sample_cnts):
                affinity = np.exp(-np.sum(np.square(samples.iloc[i] - samples.iloc[j]) / 2.0))
                affinity_matrix[i][j] = affinity_matrix[j][i] = affinity
        # print(affinity_matrix)
        return affinity_matrix


if __name__ == "__main__":
    # 需要使用下载iris数据集
    iris_df = pd.read_csv("iris.data.csv", )

    # 按类别+比例切分
    labeled_frac = 0.1
    labeled_df = pd.DataFrame()
    unlabeled_df = pd.DataFrame()
    
    for target in set(iris_df["class"].values):
        tmp = iris_df[iris_df["class"]==target]
        labeled_df = labeled_df.append(tmp[:int(tmp.shape[0]*labeled_frac)])
        unlabeled_df = unlabeled_df.append(tmp[int(tmp.shape[0]*labeled_frac):])

    print("labeled:", labeled_df.shape)
    print("unlabeled:", unlabeled_df.shape)

    label_spreading = LabelSpreading()
    assigned_df= label_spreading.process(labeled_df, unlabeled_df.iloc[:, :-1])
    ret_df = (assigned_df["class"] == unlabeled_df["class"])
    print(ret_df)
    print("accuracy: %s" % (ret_df.sum() * 1.0 / ret_df.count()))
