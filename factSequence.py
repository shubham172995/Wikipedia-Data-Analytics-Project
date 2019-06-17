#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:36:02 2018

@author: descentis
"""
import xml.etree.cElementTree as ET
from nltk import word_tokenize
from nltk.tag import pos_tag
import string
from findDiff import find_diff
import matplotlib.pyplot as plt


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def hasPunctuations(inputString):
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in inputString):
        return True
    else:
        return False
def factSequenceAnalysis(path):
     tree = ET.parse(path)
     root = tree.getroot()
     root = tree.getroot()
     yRange = 0
     #fil = open("output.txt",'w')
     result = []
     f = 0
     old_rev = []
     count_rev = 0
     total_facts = []
     #fil = open("output.txt","w");
     for rev in root.find('{http://www.mediawiki.org/xml/export-0.10/}page').findall('{http://www.mediawiki.org/xml/export-0.10/}revision'):
         count_rev+=1

         '''
         if(count_rev==3):
             break
         '''
         text = rev.find('{http://www.mediawiki.org/xml/export-0.10/}text').text;
         if(not text):
             total_facts.append(0)
             continue
         tags=["NNP","NNPS"]

         tagged_sent =  pos_tag(word_tokenize(text))
         #fil.write("TimeStamp:"+rev.find("{http://www.mediawiki.org/xml/export-0.10/}timestamp").text+"\n");
         current_rev = []
         #fil.write("TimeStamp:"+rev.find("{http://www.mediawiki.org/xml/export-0.10/}timestamp").text+"\n");
         if(f==0):
             yRev = []
             count_y = 1
             for tagged_word in tagged_sent:
                 if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                     if(tagged_word[1] in tags):
                         #fil.write(tagged_word[0]+" , ")
                         old_rev.append(str(tagged_word[0]))
                         yRev.append(count_y)
                         count_y+=1
             #fil.write("\n=====================================================================\n")
             #print(old_rev)
             total_facts.append(len(old_rev))
             if(len(old_rev)>yRange):
                 yRange = len(old_rev)
             result.append(yRev)
             f=1
         else:
             
             for tagged_word in tagged_sent:
                 if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                     if(tagged_word[1] in tags):
                         #fil.write(tagged_word[0]+" , ")
                         current_rev.append(str(tagged_word[0]))
             
             new_list = find_diff(old_rev,current_rev)
             total_facts.append(len(current_rev))
             #print(current_rev)
             yRev = new_list[0]
             if(len(current_rev)>yRange):
                 yRange = len(current_rev)
             result.append(yRev)
             old_rev = current_rev
         #print("one revision completed!!")
         #fil.write("\n=====================================================================\n")
     
     result.append(total_facts)   
     result.append(count_rev)
     return result
         #fil.write("\n=====================================================================\n")


result = factSequenceAnalysis('Veerappan.xml')

xRange = result[-1]
total_facts = result[-2]
plt.xlabel('Revisions', fontsize=12)
plt.ylabel('Addition of new words in each revision', fontsize=12)

for res in range(1,len(result)-2):
    yAxis = result[res]
    xAxis = [res+1 for i in yAxis]
    sc = [1 for i in yAxis]
    plt.scatter(xAxis,yAxis, c='b',s=sc, marker='o')
    
xAxis = [i for i in range(1,xRange+1)]
sc = [1 for i in range(1,xRange+1)]    
plt.scatter(xAxis,total_facts,c='r',s=sc,marker='o')
plt.savefig('test.png',dpi=800)
plt.show()






