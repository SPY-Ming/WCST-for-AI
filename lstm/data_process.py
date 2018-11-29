# -*- coding: utf-8 -*-
#!/usr/bin/python
import re,pickle
from tflearn.datasets.svhn import label_to_one_hot_y
import numpy as np

def generate_data_human_play():
    file1 = open('./Data_clean.txt','r',encoding='utf-8')
    
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
    
    STEP = 50
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
    
    f = open('./data_%ddim.pkl'%STEP,'wb')
    pickle.dump(dataset,f,-1)
    f.close()

def generate_data_make_rule():
    '''
    number : 0
    color : 1
    shape : 2
    none : 3
    '''
    step = 6
    dataset = []
    # 规则一：前边对的情况下，下一个预测要延续前边的结果    记忆  [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
    every_sample = [[0,1] for i in range(step)]
    print(every_sample)
    for i in range(100):
        dataset.append([every_sample,0])
    print(dataset[0])
    
    every_sample = [[1,1] for i in range(step)]
    for i in range(100):
        dataset.append([every_sample,1])
    
    every_sample = [[2,1] for i in range(step)]
    for i in range(100):
        dataset.append([every_sample,2])
        
    # 规则二：当前一个规则错的情况下，要立即变换预测    改变
    every_sample = [[0,1] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(100):
        dataset.append([every_sample,1])
    print(dataset[305])
        
    every_sample = [[0,1] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(100):
        dataset.append([every_sample,2])
    
    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(100):
        dataset.append([every_sample,0])

    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(100):
        dataset.append([every_sample,2])
    
    every_sample = [[2,1] for i in range(step-1)]
    every_sample.append([2,0])
    for i in range(100):
        dataset.append([every_sample,1])

    every_sample = [[2,1] for i in range(step-1)]
    every_sample.append([2,0])
    for i in range(100):
        dataset.append([every_sample,0])
    
    # 规则三：当前两两个规则错误的情况下，要立即选择第三个规则    策略
    
    # 规则四：当前边为空时，应该以上一个选择为主    [[3,none],[3,none],[3,none],[3,none],[3,none],[3,none]] 0/1/2
    # 规则五：当前边部分为空时，应该以上一个选择为主    [[3,none],[3,none],[3,none],[3,none],[1,0],[2,1]] 2
    

# generate_data_make_rule()
generate_data_human_play()






