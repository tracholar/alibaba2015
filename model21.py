# coding:utf-8
'''
基于模型11,20 模型融合
'''
import sklearn,pandas, pickle, os, summary, util, filter
import numpy as np

from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import f1_score
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC,SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler, PolynomialFeatures
from sklearn.lda import LDA
from sklearn.decomposition import PCA


__fname__ = os.path.basename(__file__)
__fname__ = __fname__[:__fname__.rindex('.')]

#__models__ = ['model11', 'model20']
__models__ = ['model22','model23','model24']
	
def GetData():
	
	data = pandas.read_csv('data.train.csv')
	
	Y=data['buy']
	
	X=GetFeature(data)
	


	
	return X, Y
	

def GetFeature(data):

	
	X = None
	for m in __models__:
		model = util.load_model_from_name(m)
		X0 = model.GetFeature(data)
		if X is None:
			X = pandas.DataFrame(model.GetModel().predict_proba(X0)[:,1], columns=[m])
		else:
			
			X[m] = model.GetModel().predict_proba(X0)[:,1]

	assert len(X.keys()) == len(__models__)
	
	poly = PolynomialFeatures(degree=3)
	X = poly.fit_transform(X)
	
	return pandas.DataFrame(X)

		
def GetModel():
	
	f = open('%s.model' % __fname__,'rb')
	clf = pickle.load(f)
	f.close()
	return clf

def TestModel():
	return summary.TestModel(__fname__)

	
	
if __name__ == '__main__':
	
	X, Y = GetData()

	
	feature_names = X.columns
	parms = {
	'C': [1],#np.logspace(-2,2,5),  # 
	#'lr__class_weight':[{0:1,1:.95}],#[{0:1,1:r} for r in np.linspace(1,3,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	#'lda__n_components':[50,60],
	}
	
	lr = LogisticRegression(penalty='l1')
	clf = GridSearchCV(lr, parms, scoring='f1', n_jobs=5)

	
	
	

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


