# -*- coding: utf-8 -*-

'''
Created on 2017年6月3日

@author: Chin
'''

from __future__ import division

import numpy as np
import pandas as pd


class ClassifyTree(object):

    def __init__(self):
        self.cl_tree = None


    def _shannon_ent(self, data_df, target_column="label"):
        '''
        @summary: 香农熵计算
        '''
        target_percent_df = data_df[target_column].value_counts() / data_df[target_column].count()
        return -np.sum(np.log2(target_percent_df) * target_percent_df)


    def _choose_best_feature_to_split(self, data_df, target_column="label"):
        '''
        @summary: 选择最佳分离变量
        '''
        base_entropy = self._shannon_ent(data_df, target_column)
        best_feature = None
        best_gain = 0
        for field in data_df.columns:
            if field == target_column:
                continue
            if data_df.dtypes[field] == np.object:
                # 类别变量处理
                # 将data_df按指定列field进行分组, 对每一组计算_shannon_ent,并按频率求和,即得到新的信息熵 
                # print data_df.groupby("flippers").apply(lambda x: (x.shape[0]/data_df.shape[0] * _shannon_ent(x, target_column)))
                new_entropy = data_df.groupby(field)\
                            .apply(lambda x: (x.shape[0]/data_df.shape[0] * self._shannon_ent(x, target_column)))\
                            .sum()
                new_gain = base_entropy - new_entropy
                # print("%s: %s, %s, %s" % (field, new_gain, base_entropy, new_entropy))
                if new_gain > best_gain:
                    best_gain = new_gain
                    best_feature = (field, None)
            else:
                # 连续变量的处理
                # 计算连续变量的获选划分点集合, 对每一个可能的划分情况计算entropy
                ret = data_df[field].unique()
                ret.sort()
                split_values = [(ret[i] + ret[i-1])/2 for i in range(1, len(ret))]
                for candi_split in split_values:
                    # print(candi_split)
                    left_df = data_df[data_df[field] < candi_split]
                    right_df = data_df[data_df[field] >= candi_split]
                    new_entropy = left_df.shape[0]/(left_df.shape[0]+right_df.shape[0])*self._shannon_ent(left_df, target_column) + \
                                    right_df.shape[0]/(left_df.shape[0]+right_df.shape[0])*self._shannon_ent(right_df, target_column)
                    new_gain = base_entropy - new_entropy
                    # print("%s: %s, %s, %s, %s" % (field, candi_split, new_entropy, base_entropy, new_entropy))
                    if new_gain > best_gain:
                        best_gain = new_gain
                        best_feature = (field, candi_split)
        return best_feature
        
    
    def _create_tree(self, data_df, target_column="label"):
        '''
        @summary: 创建决策树
        '''
        if data_df[target_column].unique().size == 1:
            # data_df中所有label都相同
            return data_df[target_column].unique()[0]
        if data_df.columns.size == 1:
            # data_df中没有特征可供选择, 返回数量统计最多的label
            return data_df[target_column].value_counts().argmax()
        
        best_feat, feat_value = self._choose_best_feature_to_split(data_df, target_column)
        my_tree = {best_feat:{}}
        if feat_value == None:
            # 最优切分特征为类别变量
            # 最优的类别特征不再参与下面的建树过程,需要drop掉
            for f_val in data_df[best_feat].unique():
                my_tree[best_feat]["=%s"%f_val] = \
                    self._create_tree(data_df[data_df[best_feat]==f_val].drop(best_feat, axis=1), target_column)
        else:
            # 最优切分特征为连续变量
            # 最优的类别特征可以继续参与下面的建树过程,不需要drop掉
            my_tree[best_feat]["<%s"%feat_value] = \
                    self._create_tree(data_df[data_df[best_feat]<feat_value], target_column)
            my_tree[best_feat][">%s"%feat_value] = \
                    self._create_tree(data_df[data_df[best_feat]>feat_value], target_column)
        return my_tree


    def fit(self, data_df, target_column="label"):
        '''
        @summary: 决策树训练,会调用_create_tree递归创建分类树,
                                                    会使用data_df列类型来区分类别变量和连续变量
        '''
        self.cl_tree = self._create_tree(data_df, target_column)
                      

    def predict(self, df_ser):
        '''
        @summary: 分类
        @param df_ser: pandas.core.series.Series
        '''
        return self._classify(self.cl_tree, df_ser)


    def _classify(self, in_tree, df_ser):
        '''
        @summary: 用于当前分类的分类树
        @param df_ser: pandas.core.series.Series
        '''
        feat = in_tree.keys()[0]
        sub_dict = in_tree[feat]

        sub_tree = None
        for key in sub_dict:
            if key.startswith("=") and (df_ser[feat] == key[1:]):
                # print "=", type(key[1:]), type(df_ser[feat])
                sub_tree = sub_dict[key]
            elif key.startswith("<") and (eval("%s < %s" % (df_ser[feat], key[1:]))):
                # print "<", type(key[1:]), type(df_ser[feat])
                sub_tree = sub_dict[key]
            elif key.startswith(">") and (eval("%s > %s" % (df_ser[feat], key[1:]))):
                # print ">", type(key[1:]), type(df_ser[feat])
                sub_tree = sub_dict[key]
        if isinstance(sub_tree, dict):
            return self._classify(sub_tree, df_ser)
        return sub_tree
        
    
    def show_tree(self):
        '''
        @summary: 图像展现分类树
        '''
        if self.cl_tree:          
            import treePlotter
            treePlotter.createPlot(self.cl_tree)
    
    
    def __str__(self):
        import json
        return json.dumps(self.cl_tree,encoding='utf-8',ensure_ascii=False)


if __name__ == "__main__":
    data_df = pd.read_csv("data/watermelon1.csv", 
                          index_col=0)
    ct = ClassifyTree()
    ct.fit(data_df, target_column="好瓜")
    print(ct)
    print(ct.predict(data_df.iloc[0]))
    ct.show_tree()
