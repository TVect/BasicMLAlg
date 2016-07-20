# -*- coding: utf-8 -*-

'''
Created on 2016-7-19

@author: chin
'''

import matplotlib.pyplot as plt
import numpy as np
import copy
import dis

class KD_Tree(object):
    u'''
        太复杂了，需要改进
       另外，没有实现查找最近的k个点的功能 
    '''
    def __init__(self):
        self.root = self.KD_Node()

    def _build_kdtree(self, node, in_mat, axis_id):
        # 确保中位数在数据中
        if in_mat.shape[0] % 2 == 1:
            _median = np.median(in_mat, axis=0)
        else:
            _median = np.median(in_mat[1:,], axis=0)
        left_list = []
        right_list = []
        for in_pt in in_mat:
            print in_pt[0, axis_id], _median
            if in_pt[0, axis_id] > _median[0, axis_id]:
                right_list.append(in_pt.tolist()[0])
            elif in_pt[0, axis_id] < _median[0, axis_id]:
                left_list.append(in_pt.tolist()[0])
            else:
                node.points.append(in_pt.tolist()[0])
        
        node.split_line = {"axis_id": axis_id, "value": _median[0, axis_id]}
        
        if left_list:
            left_node = self.KD_Node()
            left_node.area = copy.copy(node.area)
            left_node.area[axis_id] = (left_node.area[axis_id][0], _median[0, axis_id])
            node.left_child = left_node
            left_node.parent = node
            self._build_kdtree(left_node, np.matrix(left_list), (axis_id+1)%in_mat.shape[1])
        if right_list:
            right_node = self.KD_Node()
            right_node.area = copy.copy(node.area)
            right_node.area[axis_id] = (_median[0, axis_id], right_node.area[axis_id][1])
            node.right_child = right_node
            right_node.parent = node
            self._build_kdtree(right_node, np.matrix(right_list), (axis_id+1)%in_mat.shape[1])


    def build_kdtree(self, in_mat):
        self.root.area = [(float("-inf"), float("inf"))] * in_mat.shape[1]
        self._build_kdtree(self.root, in_mat, axis_id=0)


    def find_least_pt(self, point, k_cnt=1):
        cur_node = self.find_path_to_pt(point)[-1]
        min_dis = float("inf")
        min_pt = None
        while cur_node:
            for pt in cur_node.points:
                dis = np.sum((np.array(pt) - np.array(point)) **2)
                if min_dis > dis:
                    min_dis = dis
                    min_pt = pt
            
            line_dis = (point[cur_node.split_line["axis_id"]] - cur_node.split_line["value"])**2
            if line_dis < min_dis:
                # 需要进入cur_node的另一个子节点进行搜索
                if cur_node.left_child:
                    if pt in cur_node.left_child:
                        test_node = cur_node.right_child
                    else:
                        test_node = cur_node.left_child
                else:
                    test_node = None
                
                
                if test_node:
                    test_min_dis, test_min_pt = test_node.find_pt_closer(point)
                    if min_dis > test_min_dis:
                        min_dis = test_min_dis
                        min_pt = test_min_pt
            
            cur_node = cur_node.parent

        return min_dis, min_pt
            
                
    
    def find_path_to_pt(self, point):
        path_list = []
        cur_node = self.root
        while cur_node:
            if point in cur_node:
                path_list.append(cur_node)
            if point[cur_node.split_line["axis_id"]] < cur_node.split_line["value"]:
                cur_node = cur_node.left_child
            elif point[cur_node.split_line["axis_id"]] > cur_node.split_line["value"]:
                cur_node = cur_node.left_child
            else:
                break

        return path_list


    def show(self):
        self._show(self.root, 0)


    def _show(self, node, breaks):
        print "\t" * breaks, node.points, node.area
        if node.left_child: 
            self._show(node.left_child, breaks+1)
        if node.right_child:
            self._show(node.right_child, breaks+1)


    class KD_Node(object):

        def __init__(self):
            self.points = []
            self.parent = None
            self.left_child = None
            self.right_child = None
            self.area = None
            self.split_line = None

        def find_pt_closer(self, point):
            min_pt = None
            min_dis = float("inf")
            for pt in self.points:
                dis =  np.sum((np.array(point) - np.array(pt))**2)
                if dis < min_dis:
                    min_dis = dis
                    min_pt = pt
            if self.left_child:
                left_min_dis, left_min_pt = self.left_child.find_pt_closer(point)
                if left_min_dis < min_dis:
                    min_dis = left_min_dis
                    min_pt = left_min_pt
            if self.right_child:
                right_min_dis, right_min_pt = self.left_child.find_pt_closer(point)
                if right_min_dis < min_dis:
                    min_dis = right_min_dis
                    min_pt = right_min_pt
            return min_dis, min_pt

        def __contains__(self, point):
            for axis, pt_axis in enumerate(point):
                if self.area[axis][0] < pt_axis < self.area[axis][1]:
                    continue
                return False
            return True

        def __str__(self):
            return str(self.points) + str(self.area)

def visual_points(in_list):
    plt.scatter([2,5,9,4,8,7], [3,4,6,7,1,2], marker='x')

    plt.show()

if __name__ == "__main__":
    in_mat = np.matrix([[2, 3], [5, 4], [9, 6],
                        [4, 7], [8, 1], [7, 2]])

    kd_tree = KD_Tree()
    kd_tree.build_kdtree(in_mat)

    kd_tree.show()

    for node in kd_tree.find_path_to_pt([2, 3]): 
        print node

    min_dis, min_pt = kd_tree.find_least_pt([2, 1])
    print min_dis, min_pt
    
    print "finished..."
    visual_points(None)
    
