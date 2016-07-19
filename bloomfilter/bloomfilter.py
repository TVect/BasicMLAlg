# -*- coding: utf-8 -*-

'''
Created on 2016-7-18

@author: chin
'''

import math
from BitVector import BitVector
from GeneralHashFunctions.GeneralHashFunctions import *

all_hash_funcs = [RSHash, JSHash, PJWHash, ELFHash, BKDRHash, SDBMHash,
                  DJBHash, DEKHash, BPHash, FNVHash, APHash]

class BloomFilter(object):
    u'''
            根据误判率上限p和存储上限n,来计算得到最优的位数组长度m和hash函数个数k
        m = -n*ln(p) / (ln2*ln2)
        k = ln2 * (m/n)
            此时在满存储时，位数组中每一位为1的概率大约为1-e^(-kn/m)，即位数组的使用率大约为0.5
    '''

    def __init__(self, err_clv, storage_clv):
        '''
        @param err_clv: error ceiling limit value
        @param storage_clv: storage ceiling limit value
        '''
        self.bit_num = int(math.ceil(-storage_clv * math.log(err_clv) / math.pow(math.log(2), 2)))
        self.hash_num = int(math.ceil(self.bit_num / storage_clv * math.log(2)))
        self.hash_funcs = all_hash_funcs[:self.hash_num]
        self.bit_vector = BitVector(size=self.bit_num)

    def add(self, item):
        for hash_func in self.hash_funcs:
            hash_value = hash_func(item) % self.bit_num
            self.bit_vector[hash_value] = 1

    def __contains__(self, item):
        for hash_func in self.hash_funcs:
            hash_value = hash_func(item) % self.bit_num
            if self.bit_vector[hash_value] == 0:
                return False
        return True


if __name__ == "__main__":
    bloom_filter = BloomFilter(1.0/100, 200000)
    print bloom_filter.bit_num, bloom_filter.hash_num
    test_list = range(200000)
    
    [bloom_filter.add(str(test_item)) for test_item in test_list]

    err = 0
    for i in range(300000, 500000):
        if str(i) in bloom_filter:
            err += 1
    print "perr = ", float(err)/200000
