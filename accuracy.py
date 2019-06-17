#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 16:34:47 2018

@author: computerlab
"""
import xml.etree.cElementTree as ET
from nltk import word_tokenize
from nltk.tag import pos_tag
import string

import matplotlib.pyplot as plt

filename="dict.txt"
filename1="notfound.txt"
prime_dict={}
file1=open(filename,"r")
file2=open(filename1,"w")
for line in file1:
    words=line.split()
    prime_dict[words[0]]=words[1]
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def hasPunctuations(inputString):
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in inputString):
        return True
    else:
        return False
x=[]
y=[]
def factSequenceAnalysis(path):
     tree = ET.parse(path)
     root = tree.getroot()
     root = tree.getroot()
     
     count_rev=0
    
     for rev in root.find('{http://www.mediawiki.org/xml/export-0.10/}page').findall('{http://www.mediawiki.org/xml/export-0.10/}revision'):
         
         count_rev+=1
         file2.write("\n-----Revision----- "+str(count_rev)+"\n")
         x.append(count_rev)
         text = rev.find('{http://www.mediawiki.org/xml/export-0.10/}text').text;
         if(not text):
             
             continue
         tags=["NNP","NNPS"]

         tagged_sent =  pos_tag(word_tokenize(text))
         
         
         all_count=0
         real_count=0
         
         for tagged_word in tagged_sent:
             
             
             if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                 if(tagged_word[1] in tags):
                     all_count+=1
                     if tagged_word[0] in prime_dict.keys():
                         real_count+=1
                     else:
                         file2.write(tagged_word[0]+",")
         me=(all_count-real_count)/real_count*100
         file2.write("\n ACCURACY percentage="+str(me))
         
         y.append(me)       
factSequenceAnalysis("Veerappan.xml")
plt.xlabel('Revisions', fontsize=12)
plt.ylabel('Accuracy % w.r.t Master Graph', fontsize=12)
sc=[1 for _ in range(len(x))]
plt.scatter(x,y,c='b',s=sc,marker='o')

