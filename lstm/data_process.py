# -*- coding: utf-8 -*-
#!/usr/bin/python
import re,pickle
from tflearn.datasets.svhn import label_to_one_hot_y
import numpy as np

file1 = open('./Data2.txt','r',encoding='utf-8')

a = file1.readlines()
file1.close()
d = {'\'SHAPE\'':2,'\'COLOR\'':1,'\'NUMBER\'':0}

print('a is',a[0])
print('len of a is ',len(a))
# n = 0
# while n <= len(a):
Data = []
#     slist = a[n:n+10]
#     print(slist)
for i in a:
    i = i.strip()
    i = i.replace("(","")
    i = i.replace(")","")
    ss,right = i.split(",")
    # print('before map,ss is ',ss)
    ss = d[ss]
    # print('after map,ss is',ss)
    # print(ss,right)
    Data.append((ss,int(right)))

STEP = 3
dataset = []
for n in range(len(Data)-STEP):
    dataset.append([Data[n+STEP][0],Data[n:n+STEP]])

# for d in dataset:
#     label,feature = d
#     label = label_to_one_hot_y(label,3)
#     print(label)
#     print(type(feature))
#     print(np.shape(feature))
#     break

dataset = [(label_to_one_hot_y(d[0],3),d[1]) for d in dataset]
print('example of data ',dataset[0])
print('len of dataset',len(dataset))

f = open('./data_3dim.pkl','wb')
pickle.dump(dataset,f,-1)
f.close()










