# -*- coding: utf-8 -*-
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import random
import pickle
import collections

DEBUG = 0

#import tensorflow.contrib.slim as slim
#tf.reset_default_graph()


class Agent_wsct(object):
    def __init__(self):
        print('load Operation Net')
        self.mlp_graph = tf.Graph()
        self.sess_mlp = tf.InteractiveSession(graph=self.mlp_graph)
        with self.mlp_graph.as_default():
            saver1 = tf.train.import_meta_graph("./mlp/model/model1.meta")
            saver1.restore(self.sess_mlp, "./mlp/model/model1")
            self.mlp_x = self.mlp_graph.get_operation_by_name("Input_Data").outputs[0]
            self.mlp_y = self.mlp_graph.get_operation_by_name("Label").outputs[0]
            self.keep_prob = self.mlp_graph.get_operation_by_name("dropout_rate").outputs[0]
            self.mlp_pred = tf.get_collection('pred')[0]
            
            if DEBUG:
                np.set_printoptions(threshold=np.inf) # 解决np观察数据省略
                data=pd.read_csv('./mlp/test1001.csv')
                xs=data.values[0:10000,1:]
                ys=data.values[0:10000,0]
                classes=max(ys)+1
                one_hot_label=np.zeros(shape=(ys.shape[0],classes))
                one_hot_label[np.arange(0,ys.shape[0]),ys] = 1
                
                train_x_disorder,test_x_disorder,train_y_disorder,test_y_disorder=train_test_split(xs,one_hot_label,train_size=0.7,random_state=33)
                accuracy1 = tf.get_collection('accuracy')[0]
                output_card = self.sess_mlp.run(tf.argmax(self.mlp_pred,1),
                            feed_dict={self.mlp_x:test_x_disorder[:3],self.mlp_y:test_y_disorder[:3],self.keep_prob: 1.0})
                print('mlp pred test',output_card)
        print('Load complete!')
        
        print('Load Strategy Net')
        self.graph_lstm = tf.Graph()
        self.sess_lstm = tf.InteractiveSession(graph=self.graph_lstm)
        with self.graph_lstm.as_default():
            saver2 = tf.train.import_meta_graph("./lstm/model/lstm.meta")
            saver2.restore(self.sess_lstm, "./lstm/model/lstm")
        #     lstm_x = mlp_graph.get_operation_by_name("input_x").outputs[0]
        #     lstm_y = mlp_graph.get_operation_by_name("input_y").outputs[0]
            self.lstm_x = tf.get_collection('input_x')[0]
            self.lstm_y = tf.get_collection('input_y')[0]
            self.lstm_pred = tf.get_collection('pred')[0]
            
            if DEBUG:
                data = pickle.load(open('./lstm/data_3dim.pkl','rb'))
                train_set = data[:500]
                test_set = data[500:]
                
                x_train = np.array([t[1] for t in train_set])
                y_train = [t[0] for t in train_set]
                x_test = np.array([t[1] for t in test_set])
                y_test = [t[0] for t in test_set]
                accuracy2 = tf.get_collection('accuracy')[0]
                xt = x_test[0]
                yt = y_test[0]
                output_decision = self.sess_lstm.run(tf.argmax(self.lstm_pred,1),
                    feed_dict={self.lstm_x:xt[np.newaxis,:],self.lstm_y:yt[np.newaxis,:]})
                print('lstm pred test',output_decision)
        print('Load complete!')
        
    def run(self,situation,previous_decision):
        decision = self.sess_lstm.run(tf.argmax(self.lstm_pred,1),{self.lstm_x:[previous_decision]})
        situation.append(decision[0])
        action = self.sess_mlp.run(tf.argmax(self.mlp_pred,1),
                feed_dict={self.mlp_x:[situation],self.keep_prob:1.0})
        print('action (card choosed by agent) is ',action)
        return action,decision
    
if __name__ == "__main__":
    ''' Unit test'''
    a = Agent_wsct()
    
    if DEBUG:
        np.set_printoptions(threshold=np.inf)
        data=pd.read_csv('./mlp/test1001.csv')
        xs=data.values[0:10000,1:21]
        ys=data.values[0:10000,0]
        classes= 4
        one_hot_label=np.zeros(shape=(ys.shape[0],classes))
        one_hot_label[np.arange(0,ys.shape[0]),ys] = 1
        
        train_x,test_x,train_y,test_y=train_test_split(xs,one_hot_label,train_size=0.7,random_state=33)
        
        decision_stack = collections.deque(maxlen=3)
        for i in range(2):
            decision_stack.append([0,0])
    #     print('initial state is ',decision_stack)
        
        
        
        last_dec = 0
        last_judge = 0
        
        
        while (i<7):
            situation = test_x[i]
            
            decision_stack.append([last_dec,last_judge])
            print('init_decision ',decision_stack)
            print('state',situation)
            action,decision= a.run(situation=situation,previous_decision = decision_stack)
    #         print(action[0])
            last_dec = decision[0]
            last_judge = random.randint(0,1)
            i += 1
        
    
    
    
#     
# 
# for i in range(4):
#     a.append(i)
#     print( a)
#     
    
    
    
    
    
    
    
    
    

