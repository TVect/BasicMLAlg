# -*- coding: utf-8 -*-

'''
HMM vertibi-alg

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

S = ['D6', 'D4', 'D8']    # 状态
K = [1,2,3,4,5,6,7,8]    # 输出符号
begin_prob = np.ones(3)/3    # 初始状态概率分布
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

def viterbi(observerd_list):
    list_size = len(observerd_list)
    status_size = len(S)
    best_forward = [range(status_size)]  #记录每个状态最优前驱状态
    best_prob = (np.diag(begin_prob) * B_prob[:,observerd_list[0]-1]).T  #记录当前的各个状态的最优概率
    for i in xrange(1, list_size):
        before_after_prob = np.diagflat(best_prob)* A_prob * np.diagflat(B_prob[:, observerd_list[i]-1])
        best_prob = before_after_prob.max(axis=0)
        best_forward = np.row_stack((before_after_prob.argmax(axis=0), best_forward))
#         print best_prob
#         print best_forward
    best_status = []  #找出最优的状态序列
    best_status_insert = best_status.insert
    id = best_prob.argmax()
    for row in best_forward:
        best_status_insert(0, S[id])
        id = row[0,id]
#     print best_status
    return best_status


if __name__ == '__main__':
    print viterbi([1,6,3,5,2,7,3,5,2,4])
