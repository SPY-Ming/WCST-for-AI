# -*- coding: utf-8 -*-

import jieba

s = '今天吃什么'
print(s)
print('//'.join(jieba.cut(s)))