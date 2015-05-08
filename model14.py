# coding:utf-8
'''
增加了用户地理位置对商品的行为特征，采用RF
'''
import sklearn,pandas, pickle, os, summary, util
import numpy as np

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
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
	samples = (np.random.rand(len(Y))<0.08) | (Y==1)
	X = X[samples]
	Y = Y[samples]
	
	feature_names = X.columns
	parms = {
	'rf__n_estimators': [500], #range(30,100,5),  # (30,40,5)
	#'rf__max_features' : ['log2'], #[7] 8
	'rf__min_samples_leaf' : [15], #range(1,3), #range(2,6,2), # 15 best
	#"rf__max_depth" : [6], #range(4,10,2),  # 8  # nothing
#	'rf__max_leaf_nodes': [6], #range(15,50,4), #[20],
	#'gamma' : np.logspace(1e-3,1,4)
	#'rf__class_weight':[{0:1,1:4.}], #[{0:1,1:r} for r in np.linspace(1,1.2,5)], #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	}
	tr = ExtraTreesClassifier(n_jobs=10)
	rf = RandomForestClassifier(n_jobs=10,criterion = 'gini')
	pipe = Pipeline([('rf',rf)])
	clf = GridSearchCV(pipe, parms, scoring='f1', n_jobs=1)

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


