# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:47:02 2018

@author: 梁靖旖
"""

import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
data=pd.read_csv('./test1001.csv')
xs=data.values[0:10000,1:]
ys=data.values[0:10000,0]

classes=max(ys)+1
one_hot_label=np.zeros(shape=(ys.shape[0],classes))
one_hot_label[np.arange(0,ys.shape[0]),ys] = 1

train_x_disorder,test_x_disorder,train_y_disorder,test_y_disorder=train_test_split(xs,one_hot_label,train_size=0.7,random_state=33)



print(np.shape(test_x_disorder))
for tx in test_x_disorder:
    print('tx is ',tx)
    print(type(tx))

graph1 = tf.Graph()
sess1 = tf.InteractiveSession(graph=graph1)
with graph1.as_default():
    saver1 = tf.train.import_meta_graph("./model/model1.meta")
    saver1.restore(sess1, './model/model1')

    x = graph1.get_operation_by_name("Input_Data").outputs[0]
    y_ = graph1.get_operation_by_name("Label").outputs[0]
    keep_prob = graph1.get_operation_by_name("dropout_rate").outputs[0]
    
    m1_w1 = tf.get_collection('model1_w1')[0]
    m1_b1 = tf.get_collection('model1_b1')[0]
    m1_w2 = tf.get_collection('model1_w2')[0]
    m1_b2 = tf.get_collection('model1_b2')[0]
    print(m1_b2)
    print(type(m1_b2))
    accuracy1 = tf.get_collection('accuracy')[0]
    
    print('model1 ,accuracy1 is ',accuracy1.eval({x:test_x_disorder,y_:test_y_disorder,keep_prob: 1.0}))
    m1_w1_out,m1_b1_out,m1_w2_out,m1_b2_out  = sess1.run([m1_w1,m1_b1,m1_w2,m1_b2],feed_dict={x:test_x_disorder,y_:test_y_disorder,keep_prob: 1.0})
    print(type(m1_b2_out))

'''init graph2'''
sess2 = tf.InteractiveSession(graph=graph2)
with graph2.as_default():
    saver2 = tf.train.import_meta_graph("./model/model2.meta")
    saver2.restore(sess2, './model/model2')
    m2_w1 = tf.get_collection('model2_w1')[0]
    m2_b1 = tf.get_collection('model2_b1')[0]
    m2_w2 = tf.get_collection('model2_w2')[0]
    m2_b2 = tf.get_collection('model2_b2')[0]
    m2_w1_out,m2_b1_out,m2_w2_out,m2_b2_out  = sess2.run([m2_w1,m2_b1,m2_w2,m2_b2])

graph3 = tf.Graph()
sess3 = tf.InteractiveSession(graph=graph3)
with graph3.as_default() as g:
    x=tf.placeholder(dtype = tf.float32,shape=[None,21],name='Input_Data')
    y_=tf.placeholder(dtype = tf.float32,shape=[None,4],name='Label') 
    keep_prob = tf.placeholder(tf.float32,name = 'dropout_rate')
    
    w1 = tf.Variable(initial_value=m2_w1_out)
    b1 = tf.Variable(initial_value=m2_b1_out)
    h1 = tf.nn.relu(tf.matmul(x,w1)+b1)
     
    w2 = tf.Variable(initial_value=m2_w2_out)
    b2 = tf.Variable(initial_value=m2_b2_out)
    h2 = tf.matmul(h1,w2)+b2
    
    y = tf.nn.softmax(h2,1)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32),name = 'accuracy')
    sess3.run(tf.global_variables_initializer())
    
    print(sess3.run(b2))
    print('accuracy is ',sess3.run(accuracy,feed_dict={x:test_x_disorder,y_:test_y_disorder,keep_prob: 1.0}))
    y_out = sess3.run(tf.argmax(y,1),feed_dict={x:test_x_disorder,y_:test_y_disorder,keep_prob: 1.0})
    i=0
    while (i<5):
        print(y_out[i],np.argmax(test_y_disorder[i],0))
        i+=1











