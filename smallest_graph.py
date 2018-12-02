# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 18:47:01 2018

@author: 竹本
"""
# coding=utf8
import pandas as pd
import numpy as np
        
#map=['A,B', 'B,C', 'C,A', 'D,E', 'C,F', 'F,G']

def Generate_map_dic(map):
    '''
    构造邻接矩阵行列编号与图中节点的映射关系
    按节点在原文本中出现顺序排序
    '''
    link_2_num={}
    all_point=[]
    if not map:
        return False
    flag=0
    for con in map:
        cur = con.split(',')
        if cur[0] not in all_point :
            link_2_num[cur[0]]=flag
            all_point.append(cur[0])
            flag +=1
        if cur[1] not in all_point :
            link_2_num[cur[1]]=flag
            all_point.append(cur[1])
            flag +=1
    return link_2_num

def Generate_con_mat(map,link_2_num):
    '''
    构造邻接矩阵
    '''
    con_mat=[[0 for i in range(0,len(link_2_num))] for j in range(0,len(link_2_num))]
    for con in map :
        cur = con.split(',')
        con_mat[link_2_num[cur[0]]][link_2_num[cur[1]]] = 1
        con_mat[link_2_num[cur[1]]][link_2_num[cur[0]]] = 1
    return con_mat

def Get_sub_maps(con_mat,link_2_num):
    '''
    计算所有连通子图
    '''
    if not con_mat or len(con_mat)<2:
        return False
    sub_map = []
    nodes = []
    for i in range(len(con_mat)):
        tmp_map = []
        if i not in nodes:
            nodes.append(i)
            tmp_map.append(i)
            to_search = [i]
            while to_search:
                flag=to_search.pop()
                for j in range(len(con_mat[flag])):
                    if con_mat[flag][j]==1 and j not in nodes:
                        to_search.append(j)
                        nodes.append(j)
                        tmp_map.append(j)
            sub_map.append(tmp_map)
    #以下将数字表示映射回字母
    new_dict = {v : k for k, v in link_2_num.items()}
    new_sub_map = []
    for map in sub_map:
        sub = []
        for item in map:
            sub.append(new_dict[item])
        new_sub_map.append(sub)
    return new_sub_map

def Count_dis(con_mat,p1,p2):
    '''
    计算邻接矩阵中任意两点的距离
    返回-1代表两点间无通路连接
    采用广度优先搜索（BFS）
    '''
    to_search=[p1]
    finish_search=[]
    dis = 0
    flag=-1
    while to_search :
        tmp=[]
        for point in to_search :
            finish_search.append(point)
            cur = con_mat[point]
            for i in range(len(cur)):
                if cur[i]==1 :
                    if i == p2 :
                        dis += 1
                        return dis
                    if i not in finish_search and i not in to_search :
                        tmp.append(i)
        dis += 1
        to_search = tmp
    return flag

def Count_d_of_sub_map(link_2_num,con_mat,sub_map):
    '''
    计算连接子图的直径
    '''
    d = -1
    for i in range(len(sub_map)):
        for j in range(i+1,len(sub_map)):
            d = max(d,Count_dis(con_mat,link_2_num[sub_map[i]],link_2_num[sub_map[j]]))
    return d

# Read data
pos_data = pd.read_csv("D:\Sunmnet\pos\pos_data.csv",names = ['pos1-pos2'],encoding = 'gb2312')
pos_list = pos_data['pos1-pos2'].tolist()

link_2_num = Generate_map_dic(pos_list)
#print ('link_2_num',link_2_num)
con_mat = Generate_con_mat(pos_list,link_2_num)
#print ('con_mat',con_mat)
sub_map = Get_sub_maps(con_mat,link_2_num)
#print (sub_map) 
print ('distance of these two points is',Count_dis(con_mat,0,5))
print ('diameter of sub_map',sub_map[0],'is',Count_d_of_sub_map(link_2_num,con_mat,sub_map[0]))
print ('diameter of sub_map',sub_map[1],'is',Count_d_of_sub_map(link_2_num,con_mat,sub_map[1]))

#sub_map


















