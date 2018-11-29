# -*- coding: utf-8 -*-
import tensorflow as tf
import random
import pandas as pd
import numpy as np
import pickle




'''data process'''
step = 6
data = pickle.load(open('./data_V2_6dim.pkl','rb'))

split_num = int(len(data)*0.2)
train_set = data
test_set = random.sample(data,split_num)
print('len of train set {} ; len of test set {}'.format(len(train_set),len(test_set)))

epochs = 100
n_classes = 3
lr = 5e-3
batch_size = 1
hidden_size = 150
batch_index=[]
num_batch = len(data)

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
        output = tf.nn.dropout(output, 0.7)
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
        W = tf.nn.dropout(W,0.7)
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
        for input_feature,input_label in train_set:
            optimizer.run({input_x:[input_feature],
                           input_y:[input_label]})
        acc = []
        for xt,yt in test_set:
            acc.append(accuracy.eval({input_x:[xt],input_y:[yt]}))
        arr = np.mean(acc)
        if brr<arr:
           brr=arr
           b=i
           saver.save(sess,"./model/lstm_%idim_v1"%step)
           print('save max accuracy is {}'.format(brr))
        print('in epoch {} , accuracy is {}'.format(i,arr))
        
        
train_lstm()
# 
# 











