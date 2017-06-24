# -*- coding: utf-8 -*-

'''
Created on 2017年6月24日

@author: Chin
@summary: 周志华 机器学习 P309

'''

import pandas as pd

class ConstrainedSeedKmeans(object):
    
    def __init__(self):
        pass
    
    def process(self, labeled_df, unlabeled_df):
        '''
        @param labeled_df: 有标注的df, 标注列名为class
        @param unlabeled_df: 无标注的df, 即无class列
        @param n_clusters: 聚簇的个数
        '''
        # 初始化类中心点
        center = self.estimate_means(labeled_df)

        while True:
            assgined_df = self.assgin_cluster(center, unlabeled_df)
            new_center = self.estimate_means(pd.concat([labeled_df, assgined_df]))
            if (abs((new_center - center)/center) < 0.001).all().all():
                return assgined_df
            else:
                print("update center:", (new_center-center).sum())
                center = new_center


    def estimate_means(self, labeled_df):
        return labeled_df.groupby(labeled_df["class"]).mean()

    def assgin_cluster(self, center, unlabeled_df):
        result_df = pd.DataFrame()
        for row in unlabeled_df.iterrows():
            row[1]["class"] = (row[1] - center).applymap(lambda x: x**2).sum(axis=1).idxmin()
            result_df = result_df.append(row[1])
        return result_df


if __name__ == "__main__":
    # 需要使用下载iris数据集
    iris_df = pd.read_csv("iris.data.csv", )

    # 按类别+比例切分
    labeled_frac = 0.2
    labeled_df = pd.DataFrame()
    unlabeled_df = pd.DataFrame()
    
    for target in set(iris_df["class"].values):
        tmp = iris_df[iris_df["class"]==target]
        labeled_df = labeled_df.append(tmp[:int(tmp.shape[0]*labeled_frac)])
        unlabeled_df = unlabeled_df.append(tmp[int(tmp.shape[0]*labeled_frac):])
    
    contrained_seed_kmeans = ConstrainedSeedKmeans()
    assgined_df = contrained_seed_kmeans.process(labeled_df, unlabeled_df.iloc[:, :-1])
    result = (assgined_df["class"] == unlabeled_df["class"])
    print(result.count(), result.sum())
