# -*- coding: utf-8 -*-
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

in_units = 21 # 输入节点数
h1_units = 180 # 隐含层节点数
sess = tf.InteractiveSession()
W1 = tf.Variable(tf.truncated_normal([in_units, h1_units], stddev=0.1),name='MLP_Layer1_W') #
b1 = tf.Variable(tf.zeros([h1_units]),name='MLP_Layer1_b') # 隐含层偏置b1全部初始化为0
W3 = tf.Variable(tf.zeros([h1_units,4]),name='MLP_Layer3_W')
b2 = tf.Variable(tf.zeros([4]),name='MLP_Layer3_b')
x=tf.placeholder(dtype = tf.float32,shape=[None,21],name='Input_Data')
keep_prob = tf.placeholder(tf.float32,name = 'dropout_rate') # Dropout失活率
#print(W2)
# 定义模型结构
hidden1 =tf.nn.relu(tf.matmul(x, W1) + b1,name='MLP_Hidden1')
hidden1_drop =tf.nn.dropout(hidden1, keep_prob,name='MLP_Hidden1_Dropout')
y =tf.nn.softmax(tf.matmul(hidden1_drop, W3) + b2,name='Out_Put')

# 训练部分
y_=tf.placeholder(dtype = tf.float32,shape=[None,4],name='Label') 
##定义损失函数
tf.add_to_collection('model1_w1',W1)
tf.add_to_collection('model1_b1',b1)
tf.add_to_collection('model1_w2',W3)
tf.add_to_collection('model1_b2',b2)

loss_function =tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y), reduction_indices=[1]))
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32),name = 'accuracy')
tf.add_to_collection('accuracy',accuracy)
tf.add_to_collection('pred',y)

global_step = tf.Variable(0, name="global_step", trainable=False)
optimizer = tf.train.AdamOptimizer(5e-3).minimize(loss_function, global_step)
# grads_and_vars = optimizer.compute_gradients(loss_function)


saver=tf.train.Saver(max_to_keep = 1)
brr=0
# 定义一个InteractiveSession会话并初始化全部变量
tf.global_variables_initializer().run()
for i in range(2000):
    optimizer.run({x:train_x_disorder,y_:train_y_disorder, keep_prob:1})
    if i % 100 == 0:
       print('第',i,'轮迭代后：')
       arr=accuracy.eval({x:test_x_disorder,y_:test_y_disorder,keep_prob: 1.0})
       print(accuracy.eval({x:test_x_disorder,y_:test_y_disorder,keep_prob: 1.0}))
       saver.save(sess, "./model/model1")
#            saver.save(sess, "./model/model.ckpt")
       print('save success')
# print('第',b,'轮迭代后：')
# print(brr,' 效果最佳')
print(sess.run(b2))


