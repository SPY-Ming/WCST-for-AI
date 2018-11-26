# -*- coding: utf-8 -*-
import numpy as np

f = open('./test.txt','r')
data = f.readlines() #将txt文件中的数据按行读取
f.close()

features = [] # 特征集
labels = [] # 标签集

for d in data:
    d = d.strip() #去掉字符串收尾行的回车
    print(d)
    label,feature = d.split('\t') # 将字符串按照 '\t' 符号进行切分
#     print(label,feature)
    feature = feature.split(',') # 将字符串按照',' 符号进行切分
    feature = [int(f) for f in feature] #将feature中的每一个元素转换成int形式
    labels.append(int(label)) # 将label从字符串形式转换成int形式并添加到标签集中
    features.append(tuple(feature)) #将feature转换成tuple形式并添加到标签集中
 
for l,f in zip(labels,features):
    print(l,f)

feature = np.array(feature)
print(type(feature))
print('before trans to set',len(features))
features = set(features) # 将feature转换成set形式。使用set删除重复的数据
print('after trans to set',len(features))

# set 效果演示
a = [1,2,3,4,5,6,5,4,3,2]
print(len(a))
a= set(a)
print(a)
print(len(a))


