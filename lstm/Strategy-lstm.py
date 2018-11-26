# -*- coding: utf-8 -*-
import tensorflow as tf
import random
import pandas as pd
import numpy as np
import pickle

'''data process'''
data = pickle.load(open('./data_3dim.pkl','rb'))
train_set = data[:500]
test_set = data[500:]

x_train = np.array([t[1] for t in train_set])
y_train = [t[0] for t in train_set]
x_test = np.array([t[1] for t in test_set])
y_test = [t[0] for t in test_set]



epochs = 100
n_classes = 3
lr = 5e-3
batch_size = 1
hidden_size = 100
batch_index=[]
num_batch = len(x_train)
step = 3

sess = tf.InteractiveSession()

def LSTM_model(inputs, hidden_size, batch_size):
    lstm = tf.contrib.rnn.LSTMCell(hidden_size, forget_bias=1.0)
    state = lstm.zero_state(batch_size, tf.float32)
    outputs, state = tf.nn.dynamic_rnn(
        lstm, inputs,
        initial_state=state,
        dtype=tf.float32)
    return outputs
 
def train_lstm ():
    # build model
    input_x = tf.placeholder('float', [None, step, 2],name='input_x')
    input_y = tf.placeholder('float', [None, 3],name='input_y')

    # LSTM Network
    with tf.variable_scope('lstm_layer'):
        output = LSTM_model(input_x,hidden_size,batch_size,)
        output = tf.nn.dropout(output, 0.76)
        print('lstm output is ',output)
        output = output[:,-1,:]
        print('last output is ',output)
    with tf.variable_scope('output_layer'):
        W = tf.get_variable(
            "W",
            shape=[hidden_size, n_classes],
            initializer=tf.contrib.layers.xavier_initializer())
        print("W shape ", W.get_shape())
        b = tf.get_variable("b", shape=[n_classes], initializer=tf.constant_initializer(0.1))
    score = tf.add(tf.matmul(output,W),b)
    pred = tf.nn.softmax(score,1)
    loss = tf.reduce_mean(-tf.reduce_sum(input_y * tf.log(pred), reduction_indices=[1]))
 
    #accuracy
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(input_y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    optimizer = tf.train.AdamOptimizer(lr).minimize(loss)
    
    tf.add_to_collection('input_x',input_x)
    tf.add_to_collection('input_y',input_y)
    tf.add_to_collection('accuracy',accuracy)
    tf.add_to_collection('pred',pred)
    # 定义一个InteractiveSession会话并初始化全部变量
    saver=tf.train.Saver(max_to_keep = 1)
    brr=0
    tf.global_variables_initializer().run()
    for i in range(epochs):
        for input_feature,input_label in zip(x_train,y_train):
#             print(np.shape(input_feature[np.newaxis,:]))
#             print(input_label)
            print(type(input_feature))
            optimizer.run({input_x:input_feature[np.newaxis,:],
                           input_y:input_label[np.newaxis,:]})
        acc = []
        for xt,yt in zip(x_test,y_test):
            acc.append(accuracy.eval({input_x:xt[np.newaxis,:],input_y:yt[np.newaxis,:]}))
        arr = np.mean(acc)
        if brr<arr:
           brr=arr
           b=i
           saver.save(sess,"./model/lstm")
           print('save max accuracy is {}'.format(brr))
        print('in epoch {} , accuracy is {}'.format(i,arr))
        
        
train_lstm()
# 
# 











