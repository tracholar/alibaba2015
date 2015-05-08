# coding:utf-8

from createFeature import *
from gen_data import *
import pickle, sys

if not sys.path.isfile('feature_total.csv'):
	GenFeature(finput='tianchi_mobile_recommend_train_user.csv', foutput = 'feature_total.csv', lastday = '2014-12-18')

f = open('model1.model', 'rb')
clf = pickle.load(f)
f.close()





