# coding:utf-8
from __future__ import division
import util,com, sys, os
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
import pandas as pd 
import numpy as np








def GetData():
	data = pd.read_csv(r'd:\zuoyuan\alibaba\csv\featureTEST_2014-12-12.csv')
	data = data[np.random.rand(len(data))<.01]
	
	label = pd.read_csv(r'd:\zuoyuan\alibaba\csv\label_2014-12-13.csv')
	data = data.merge(label, how='left')
	
	Y = data.buy.fillna(0)
	X = GetFeature(data)
	
	return X,Y
	
	
def GetFeature(data):
	fn = [i for i in data.columns if i not in ['user_id','item_id', 'buy']]
	data.assign(user_conver_rate=lambda x: x.user_buy_count/x.user_click_count)
	df = data[fn].apply(lambda x: np.log(x+1), axis=1)
	return df
	
	


	
if __name__ == '__main__':
	X,Y = GetData()
	
	
	
	model_file = '%s.model' % util.file_basename(__file__)
	if not os.path.exists(model_file):
		lr = LogisticRegression(penalty='l1')
		lr.fit(X,Y)
		util.save_obj(lr, model_file)
	else:
		lr = util.load_obj(model_file)
	
	fn = X.columns.values 
	pred = lr.predict_proba(X)[:,1]
	for i in range(len(fn)):
		print fn[i], lr.coef_[0][i]
	print f1_score(Y,pred>.5), roc_auc_score(X,pred)
	
	
	
	