# coding:utf-8

import sklearn,pandas,pickle
import numpy as np

from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import f1_score
from sklearn.grid_search import GridSearchCV

def GetData():
	data = pandas.read_csv('data.train.csv')
	X = GetFeature(data)
	Y=data['buy']
	return X,Y 
	
def GetFeature(data):
	
	X=np.log(1+data[['user_item_lastday_count','user_item_count']])
	X2 = data[['user_item_lastday_cart_nobuy','user_geo_o']]
	X = pandas.concat([X, X2], axis=1)
	return X
def GetModel():
	f = open('model1.model','rb')
	clf = pickle.load(f)
	f.close()
	return clf

if __name__ == '__main__':
	
	
	X,Y = GetData()
	samples = (np.random.rand(len(Y))<0.06) | (Y==1)
	X = X[samples]
	Y = Y[samples]
	
	
	parms = {
	'C':np.logspace(-3,0,10),
	#'class_weight':[{0:1,1:200}] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	}
	lr = LogisticRegression()
	clf = GridSearchCV(lr, parms, scoring='f1', n_jobs=10)

	clf.fit(X,Y)
	
	import pickle
	f = open('model1.model','wb')
	pickle.dump(clf, f)
	f.close()
	

	pred = clf.predict(X)
	
	from summary import summary,clf_summary,TestModel
	clf_summary(clf)
	summary(Y, pred)
	TestModel('model1')
