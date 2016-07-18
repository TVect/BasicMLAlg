# -*- coding: utf-8 -*-

'''
Created on 2016-7-18

@author: chin
'''

import math
from GeneralHashFunctions.GeneralHashFunctions import *

all_hash_funcs = [RSHash, JSHash, PJWHash, ELFHash, BKDRHash, SDBMHash,
                  DJBHash, DEKHash, BPHash, FNVHash, APHash]

class BloomFilter(object):
    def __init__(self, err_clv, storage_clv):
        '''
        @param err_clv: error ceiling limit value
        @param storage_clv: storage ceiling limit value
        '''
        self.bit_num = int(math.ceil(-storage_clv * math.log(err_clv) / math.pow(math.log(2), 2)))
        self.hash_num = int(math.ceil(self.bit_num / storage_clv * math.log(2)))
        print self.bit_num, self.hash_num
        self.hash_funcs = all_hash_funcs[:self.hash_num]
        print self.hash_funcs
    

if __name__ == "__main__":
    BloomFilter(1.0/10000, 200000)
