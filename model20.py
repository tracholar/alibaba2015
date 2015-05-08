# coding:utf-8
'''
增加了用户地理位置对商品的行为特征
和模型13一样，只是加了数据过滤规则
'''
import sklearn,pandas, pickle, os, summary, util, filter
import numpy as np

from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import f1_score
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler
from sklearn.lda import LDA
from sklearn.decomposition import PCA
import model16
from filter import *
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier, export

__fname__ = os.path.basename(__file__)
__fname__ = __fname__[:__fname__.rindex('.')]
	
def GetData():
	
	data = pandas.read_csv('data.train.csv')

	
	Y=data['buy']
	
	X=GetFeature(data)
	
	
	
	
	#rand = np.random.rand(len(Y))<0.0001
	#idx = (Y==1) | ((Y==0) & rand)
	
	#X = X[idx]
	#Y = Y[idx]

	
	return X, Y
	

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


	samples = (np.random.rand(len(Y))<0.1) # | (Y==1)
	X = X[samples]
	Y = Y[samples]
	
	feature_names = X.columns
	parms = {
	'max_depth': [4], #np.logspace(-2,2,5),  # 
	'min_samples_leaf': [10],
	'class_weight': [{0:1,1:r} for r in np.linspace(1,10,10)]
	#'lr__class_weight':[{0:1,1:.95}],#[{0:1,1:r} for r in np.linspace(1,3,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	#'lda__n_components':[50,60],
	}
	t = DecisionTreeClassifier()
	clf = GridSearchCV(t, parms, scoring='f1', n_jobs=10)

	

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


