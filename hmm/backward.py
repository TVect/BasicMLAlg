# -*- coding: utf-8 -*-

'''
HMM backward-alg

Problem:
假设手里有三个丌同的骰子
第一个骰子是我们平常见的骰子（称这个骰子为D6），6个面，每个面（1，2，3，4，5，6）出现的概率是1/6
第二个骰子是个四面体（称这个骰子为D4），每个面（1，2，3，4）出现的概率是1/4
第三个骰子有八个面（称这个骰子为D8），每个面（1，2，3，4，5，6，7，8）出现的概率是1/8

假设我们开始掷骰子，我们先从三个骰子里挑一个，挑到每一个骰子的概率都是1/3

在我们这个例子里，D6的下一个状态是D4，D6，D8的概率都是1/3
D4，D8的下一个状态是D4，D6，D8的转换概率也都一样是1/3

'''

import numpy as np

S = ['D6', 'D4', 'D8']  # 状态
K = [1,2,3,4,5,6,7,8]   # 输出符号
begin_prob = np.ones(3)/3   # 初始状态概率分布
B_prob = np.matrix([    # 发射概率矩阵
        [1.0/6, 1.0/6, 1.0/6, 1.0/6, 1.0/6, 1.0/6,     0,     0],
        [1.0/4, 1.0/4, 1.0/4, 1.0/4,     0,     0,     0,     0],
        [1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8]
    ])
A_prob = np.matrix([    # 状态转移矩阵
        [1.0/3, 1.0/3, 1.0/3],
        [1.0/3, 1.0/3, 1.0/3],
        [1.0/3, 1.0/3, 1.0/3]
    ])

def calc_observed_prob(observed_list):
    status_count = len(S)
    beta = [1.0]*len(S)
    for value in observed_list[-1:0:-1]:
        id = value -1
        beta = [sum([A_prob[i, j] * B_prob[j, id] * beta[j] for j in range(status_count)]) 
                    for i in range(status_count)]
    result = sum(begin_prob[id] * B_prob[id, observed_list[0]-1] * beta[id] 
                 for id in range(status_count))
    print result

if __name__ == '__main__':
    calc_observed_prob([1,6,3,5,2,7,3,5,2,4])
