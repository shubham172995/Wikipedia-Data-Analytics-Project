#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 19:52:53 2018

@author: computerlab
"""

import networkx as nx
import collections
import matplotlib.pyplot as plt
from math import log
import time

file1=open("graph_modified.txt","r")
t1=time.time()
g=nx.Graph()

for line in file1:
    words=line.split()
    l1=[]
    for ele in words:
        int_ele=int(ele)
        l1.append(int_ele)
    t1=tuple(l1)
    l2=[t1]
    g.add_weighted_edges_from(l2)
t=time.time()    
#print("Graph making complete and it took",(t-t1))


degree_sequence = sorted([d for n, d in g.degree()], reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
deg=[log(y,10) for y in deg]
cnt=[log(y,10) for y in cnt]
plt.plot(deg, cnt, color='b')
plt.axis([0, 5, 0, 3])
plt.title("Degree Distribution Graph")
plt.ylabel("log(Number of nodes)")
plt.xlabel("log(Degree)")




#plt.savefig('highres_v2.png',dpi=2000)
plt.show()
file1.close()