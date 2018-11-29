# -*- coding: utf-8 -*-
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import random
import pickle
import collections
from tflearn.datasets.svhn import label_to_one_hot_y

DEBUG = 1

class Agent_wsct(object):
    def __init__(self):
        print('Load Strategy Net')
        self.graph_lstm = tf.Graph()
        self.sess_lstm = tf.InteractiveSession(graph=self.graph_lstm)
        with self.graph_lstm.as_default():
            saver2 = tf.train.import_meta_graph("./model/lstm_6dim_v1.meta")
            saver2.restore(self.sess_lstm, "./model/lstm_6dim_v1")
        #     lstm_x = mlp_graph.get_operation_by_name("input_x").outputs[0]
        #     lstm_y = mlp_graph.get_operation_by_name("input_y").outputs[0]
            self.lstm_x = tf.get_collection('input_x')[0]
            self.lstm_y = tf.get_collection('input_y')[0]
            self.lstm_pred = tf.get_collection('pred')[0]
        print('Load complete!')
        
        
if __name__ == "__main__":
    ''' Unit test'''
#     test_data = [
#     [[1,0],[2,0],[0,1],[0,1],[0,1],[0,1]], # 0
#     [[1,0],[2,1],[2,1],[2,1],[2,1],[2,1]], # 2
#     [[0,0],[1,1],[1,1],[1,1],[1,0],[0,0]], # 2
#     [[1,1],[1,1],[1,1],[1,1],[1,1],[1,0]], # 0/2
#     [[1,0],[0,1],[0,1],[0,1],[0,0],[2,1]], # 2
#     [[1,0],[0,1],[0,1],[1,0],[0,1],[0,1]], # 0
#     ]
    step = 50 
    test_data=[]
    every_sample = [[0,1] for i in range(step)] 
    test_data.append(every_sample) # 0
    every_sample = [[1,1] for i in range(step-2)]
    every_sample.append([1,0])
    every_sample.append([2,0])
    test_data.append(every_sample) # 0
    every_sample = [[1,1] for i in range(step-1)]
    every_sample.append([1,0])
    test_data.append(every_sample) # 0/2
    every_sample = [[1,1] for i in range(step-1)]
    every_sample.insert(3, [1,0])
    test_data.append(every_sample) # 1
#     for t in test_data:
#         print(t)
#     print(np.shape(test_data))
    
    f = open('./data_V2_6dim.pkl','rb')
    dataset = pickle.load(f)
        
    decision_stack = collections.deque(maxlen=6)
    a = Agent_wsct()
#     dataset.append([[[3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [0, 0]],label_to_one_hot_y(1,3)])
#     dataset.append([[[3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [1, 0]],label_to_one_hot_y(1,3)])
#     dataset.append([[[3, 3], [3, 3], [3, 3], [3, 3], [1, 0], [0, 0]],label_to_one_hot_y(1,3)])
#     dataset.append([[[3, 3], [3, 3], [3, 3], [1, 0], [0, 0], [1, 0]],label_to_one_hot_y(1,3)])
#     dataset.append([[[3, 3], [3, 3], [1, 0], [0, 0], [1, 0], [0, 0]],label_to_one_hot_y(1,3)])
    print('history decision \t decision \t label')
    results=[]
    
    test_data = random.sample(dataset,int(len(dataset)*0.2))
    for x,y in dataset:
        cc = a.sess_lstm.run(a.lstm_pred,feed_dict={a.lstm_x:[x]})
#         print(cc)
        correct_prediction = tf.equal(tf.argmax(a.lstm_pred, 0), tf.argmax(y, 0))
        res = a.sess_lstm.run(correct_prediction,feed_dict={a.lstm_x:[x],a.lstm_y:[y]})
        results.append(res)
    accuracy = np.mean(results,0)
    print(accuracy)








