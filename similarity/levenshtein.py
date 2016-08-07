# -*- coding: utf-8 -*-

'''
编辑距离
动态规划公式如下：
if i == 0 and j == 0 : 
    edit(i, j) = 0
if i == 0 and j > 0 : 
    edit(i, j) = j
if i > 0 and j == 0 : 
    edit(i, j) = i
if i ≥ 1 and j ≥ 1 : 
    edit(i, j) == min( edit(i-1, j) + 1, 
                       edit(i, j-1) + 1, 
                       edit(i-1, j-1) + f(i, j) )
    # 当第一个字符串的第i个字符不等于第二个字符串的第j个字符时，f(i, j) = 1；否则，f(i, j) = 0。
'''

import numpy as np

def edit_distance(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    edit_lists = np.zeros((len1+1, len2+1))
    edit_lists[0, 1:] = np.arange(1, len2+1)
    edit_lists[1:, 0] = np.arange(1, len1+1)
    for i in range(1, len1+1):
        for j in range(1, len2+1):
            edit_lists[i, j] = min(edit_lists[i-1, j]+1, 
                                   edit_lists[i, j-1]+1, 
                                   edit_lists[i-1, j-1]+(str1[i-1]!=str2[j-1]))
#     print edit_lists
    return edit_lists[-1, -1]


def norm_edit_distance(str1, str2):
    return edit_distance(str1, str2) / max(len(str1), len(str2))


if __name__ == "__main__":
    print norm_edit_distance("sailn", "failing")
    