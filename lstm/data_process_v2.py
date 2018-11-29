# -*- coding: utf-8 -*-
#!/usr/bin/python
import re,pickle
from tflearn.datasets.svhn import label_to_one_hot_y
import numpy as np
import random


def generate_data_make_rule():
    '''
    number : 0
    color : 1
    shape : 2
    none : 3
    '''

    num_sample = 10
    step = 6
    dataset = []
    # 规则一：前边对的情况下，下一个预测要延续前边的结果    记忆  [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
    every_sample = [[0,1] for i in range(step)]
    for i in range(num_sample):
        dataset.append([every_sample,0])
        
    every_sample = [[1,1] for i in range(step)]
    for i in range(num_sample):
        dataset.append([every_sample,1])
    
    every_sample = [[2,1] for i in range(step)]
    for i in range(num_sample):
        dataset.append([every_sample,2])
        
    # 规则二：当前一个规则错的情况下，要立即变换预测    改变
    every_sample = [[0,1] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample,1])
    # print(dataset[305])
        
    every_sample = [[0,1] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample,2])
    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample,0])

    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample,2])
    every_sample = [[0,1] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample,1])
    # print(dataset[305])

    every_sample = [[0,1] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample,2])

    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample,0])

    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample,2])

    every_sample = [[2,1] for i in range(step-1)]
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample,1])

    every_sample = [[2,1] for i in range(step-1)]
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample,0])
    
    # 规则三：当前两个规则错误的情况下，要立即选择第三个规则    策略
    every_sample = [[0,1] for i in range(step-2)]
    every_sample.append([0,0])
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample,2])
    # print(dataset[904])

    every_sample = [[0,1] for i in range(step-2)]
    every_sample.append([0,0])
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample,1])

    every_sample = [[1, 1] for i in range(step - 2)]
    every_sample.append([1, 0])
    every_sample.append([0, 0])
    for i in range(num_sample):
        dataset.append([every_sample,2])

    every_sample = [[1, 1] for i in range(step - 2)]
    every_sample.append([1,0])
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample, 0])

    every_sample = [[2, 1] for i in range(step - 2)]
    every_sample.append([2,0])
    every_sample.append([0,0])
    for i in range(num_sample):

        dataset.append([every_sample, 1])

    every_sample = [[2, 1] for i in range(step - 2)]
    every_sample.append([2,0])
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample, 0])

    # 规则四：当前边为空时，应该以上一个选择为主    [[3,none],[3,none],[3,none],[3,none],[3,none],[3,none]] 0/1/2
    every_sample = [[3,3] for i in range(step)]
    for i in range(num_sample):
        dataset.append([every_sample, 1])
    every_sample = [[3, 3] for i in range(step)]
    for i in range(num_sample):
        dataset.append([every_sample, 2])
    every_sample = [[3, 3] for i in range(step)]
    for i in range(num_sample):
        dataset.append([every_sample, 0])

    # 前边五维为空，最后一维判断错误
    every_sample = [[3, 3] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample, 1])

    every_sample = [[3, 3] for i in range(step-1)]
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample, 2])

    every_sample = [[3, 3] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample, 0])    
    
    every_sample = [[3, 3] for i in range(step-1)]
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample, 2])    
    
    every_sample = [[3, 3] for i in range(step-1)]
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample, 0])     
    
    every_sample = [[3, 3] for i in range(step-1)]
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    # 前四维为空，后两维正确
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
    
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    # 前四维为空，后两维第一步选错，第二步选正确
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([2,0])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([2,0])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([1,0])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
    
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([1,0])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    # 前四维为空，后两维选错    
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([0,0])
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([0,0])
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample, 1])

    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([1,0])
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([1,0])
    every_sample.append([2,0])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([2,0])
    every_sample.append([1,0])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
        
    every_sample = [[3, 3] for i in range(step-2)]
    every_sample.append([2,0])
    every_sample.append([0,0])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    # 前三维为空，后三维全正确
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])  
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])  
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
    
    # 前三位为空，后三维第一个错，第二个正确
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
    
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([1,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
    
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([1,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
    
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([2,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])   
    
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([2,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0]) 
    
    # 前三维为空，后三维第一个错，第二个错，第三个正确
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([2,0])
    every_sample.append([1,0])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0]) 

    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([2,0])
    every_sample.append([0,0])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1]) 
        
    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([1,0])
    every_sample.append([2,0])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0]) 

    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([1,0])
    every_sample.append([0,0])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2]) 

    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,0])
    every_sample.append([1,0])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2]) 

    every_sample = [[3, 3] for i in range(step-3)]
    every_sample.append([0,0])
    every_sample.append([2,0])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
    
    # 前二维决策为空，后四维两个错误
    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([0,0])
    every_sample.append([2,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([2,0])
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])
        
    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([1,0])
    every_sample.append([2,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])        
        
    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([2,0])
    every_sample.append([1,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])         
        
    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([0,0])
    every_sample.append([1,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])     

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([1,0])
    every_sample.append([0,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2]) 

    # 前两维为空，后四维一个错误
    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([1,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0]) 

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([1,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])    

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])  

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([0,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])  

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([2,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])  

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([2,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])  

    every_sample = [[3, 3] for i in range(step-4)]
    every_sample.append([2,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])  

    # 前一维为空，后四维两个错
    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([2,0])
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])  

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([0,0])
    every_sample.append([2,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])  

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([1,0])
    every_sample.append([2,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([2,0])
    every_sample.append([1,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([0,0])
    every_sample.append([1,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([1,0])
    every_sample.append([0,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])

    # 第一维空，后两位1个错
    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([1,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([1,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([0,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([0,0])
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    every_sample.append([1,1])
    for i in range(num_sample):
        dataset.append([every_sample, 1])

    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([2,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
    
    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([1,0])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    every_sample.append([0,1])
    for i in range(num_sample):
        dataset.append([every_sample, 0])
    
    every_sample = [[3, 3] for i in range(step-5)]
    every_sample.append([1,0])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    every_sample.append([2,1])
    for i in range(num_sample):
        dataset.append([every_sample, 2])
        
    # 随机选择数据，并生成数据集
#     f = open('./data_V2_6dim.pkl','wb')
#     print('number of sample in dataset is ',len(dataset))
#     random.shuffle(dataset)
#     one_hot_dict = {
#         0:[1,0,0],
#         1:[0,1,0],
#         2:[0,0,1]
#         }
#     for d in dataset:
#         print(d[1])
#         d[1] = one_hot_dict[d[1]]
#         print(d[1],np.argmax(d[1], 0))
#         
#     pickle.dump(dataset,f,-1)
    f.close()

    return dataset

dataset = generate_data_make_rule()
print('various of data,',len(dataset)/10)
for d in dataset:
    print(d[0],np.argmax(d[1], 0))





