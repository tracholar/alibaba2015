# coding:utf-8
# 特征分析
import numpy as np
import pandas as pd 
from matplotlib.pyplot import *


data = pd.read_csv('data.train.csv')

var = np.log(.3+data['item_buy_count'])
#var = np.exp(var)
bins = np.linspace(min(var),max(var)*1.01,100)
log_likehood = []
num = []
for i in range(1,len(bins)):
    candidate = data[(var<bins[i]) & (var>=bins[i-1])]
    likehood = np.sum(candidate['buy']==1)*1.0/(1+np.sum(candidate['buy']==0))
    log_likehood.append((likehood))
    num.append(len(candidate))
semilogy(bins[1:],log_likehood,'ro')
show()
semilogy(bins[1:],(1+np.array(num)),'ro')
show()
