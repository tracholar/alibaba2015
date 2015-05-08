# coding:utf-8
'''
Gradien Boosting
'''
import sklearn,pandas, pickle, os, summary, util
import numpy as np

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.metrics import f1_score
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import  LogisticRegression

import model16

__fname__ = os.path.basename(__file__)
__fname__ = __fname__[:__fname__.rindex('.')]
	
def GetData():
	
	data = pandas.read_csv('data.train.csv')
	
	Y=data['buy']
	
	X=GetFeature(data)
	
	
	return X, Y
	
_feature_names = model16._feature_names
def GetFeature(data):

	
	
	
	return model16.GetFeature(data)
		
def GetModel():
	
	f = open('%s.model' % __fname__,'rb')
	clf = pickle.load(f)
	f.close()
	return clf

def TestModel():
	return summary.TestModel(__fname__)
	
if __name__ == '__main__':
	
	X, Y = GetData()
	samples = (np.random.rand(len(Y))<0.25) | (Y==1)
	X = X[samples]
	Y = Y[samples]
	
	feature_names = X.columns
	parms = {
		'n_estimators' : [200],
		'max_leaf_nodes' : [3],
		'learning_rate' : [.05],
		'min_samples_leaf' : [6],
		
	}
	#tr = ExtraTreesClassifier(n_jobs=10)
	gb = GradientBoostingClassifier(init=LogisticRegression())
	pipe = Pipeline([('gb',gb)])
	clf = GridSearchCV(gb, parms, scoring='f1', n_jobs=10)

	clf.fit(X,Y)
	
	import pickle
	f = open('%s.model' % __fname__,'wb')
	pickle.dump(clf, f)
	f.close()
	
	
	
	pred = clf.predict(X)
	
	summary.clf_summary(clf, feature_names)
	summary.summary(Y, pred)
	
	
	F1, P, R = TestModel()
	
	util.notify_me('%s.F1:%.2f,P:%.2f,R:%.2f' % (__fname__, F1*100, P*100, R*100))


