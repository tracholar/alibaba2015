# coding:utf-8
'''
增加了用户地理位置对商品的行为特征
和模型13一样，只是加了数据过滤规则
'''
import sklearn,pandas, pickle, os, summary, util, filter
import numpy as np

from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler
from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
import model11
from features import *


__fname__ = os.path.basename(__file__)
__fname__ = __fname__[:__fname__.rindex('.')]
	
def GetData():
	
	data = pandas.read_csv('data.train.csv')
#	data = filter.FilterDataWithRule(data, filter.RobotRule)
	Y=data['buy']
	
	X=GetFeature(data)
	
	
	
	
	#rand = np.random.rand(len(Y))<0.0001
	#idx = (Y==1) | ((Y==0) & rand)
	
	#X = X[idx]
	#Y = Y[idx]

	
	return X, Y
	

_feature_names = allfeatures
log_features = [i for i in _feature_names if i in log_features]
factor_features = [i for i in _feature_names if i in factor_features]
signed_log_features = [i for i in _feature_names if i in signed_log_features]
linear_features = [ i for i in _feature_names if i in linear_features]
_feature_names = log_features + factor_features + signed_log_features + linear_features

def GetFeature(data):

	
	
	data['item_share_major'] = (data['item_buy_count']/(1+data['cat_buy_count']))>.2
	data['user_die'] = ((data['user_lastday_count'])<3)
	data['user_item_last2day_cart_nobuy'] = ((data['user_item_last2day_add_car']>0) & (data['user_item_last2day_buy']==0)& (data['user_item_lastday_buy']==0)).astype(int)
	data['user_item_last3day_cart_nobuy'] = ((data['user_item_last3day_add_car']>0) & (data['user_item_last3day_buy']==0)& (data['user_item_lastday_buy']==0) & (data['user_item_last2day_buy']==0)).astype(int)
	data['user_convert_rate'] = 10*(data['user_buy_count']/(1+data['user_action_count']+data['user_buy_count']*10+data['user_add_car']*5+data['user_add_star']*5))
	data['item_convert_rate'] = 10*(data['item_buy_count']/(1+data['item_click_count']+data['item_buy_count']*10+data['item_added_car']*10+data['item_added_start']*5))
	data["user_is_robot"] = filter.RobotRule(data).astype(int)
	
	X1 = np.log(.3+data[log_features])
	
#	X1['user_item_count'] = - (X1['user_item_count']-4)**2
#	X1['user_action_count'] = - (X1['user_action_count']-5)**2
#	X1['user_cat_lastday_count'] = - (X1['user_cat_lastday_count']-4)**2
	X1['user_cat_buy'] = np.log(1+data['user_cat_lastday_buy'] + data['user_cat_lastweek_buy'])
	X1['user_lastday_add_cart'] = np.log(0.3+ data['user_lastday_add_cart'] * (0.3+data['user_item_lastday_cart_nobuy']))  # 带权值用户最后一天的加购物车数目
	
	X2 = data[factor_features]
	X3 = data[linear_features]
	
#	X3['user_convert_rate'] = np.log(1e-4 + X3['user_convert_rate'])
	
	X4 = np.copysign(np.log(.3+np.abs(data[signed_log_features])),np.sign(data[signed_log_features]))
	
	X4['user_cat_aveThreeDayDelta_click'] = (lambda x:(x+6)*x*(x-6))(X4['user_cat_aveThreeDayDelta_click'])
	X4['user_item_aveThreeDayDelta_click'] = (lambda x:np.abs(x))(X4['user_item_aveThreeDayDelta_click'])
	
	
	X = pandas.concat([X1, X2,X3, X4], axis=1)
	
	
	# transformer = sklearn.preprocessing.MinMaxScaler()
	# X = transformer.fit_transform(X[_feature_names])

	return X[_feature_names]

		
def GetModel():
	
	f = open('%s.model' % __fname__,'rb')
	clf = pickle.load(f)
	f.close()
	return clf

def TestModel():
	return summary.TestModel(__fname__)

	
	
if __name__ == '__main__':
	
	X, Y = GetData()


	samples = (np.random.rand(len(Y))<0.12) | (Y==1)
	X = X[samples]
	Y = Y[samples]
	
	feature_names = X.columns
	parms = { 

	'max_leaf_nodes': [2],
	'class_weight':[{0:1,1:2}],
	
	}
	tr = StandardScaler()
	#lda = PCA(n_components=40)
	T = DecisionTreeClassifier()
	clf = GridSearchCV(T, parms, scoring='f1', n_jobs=1)

	
	
	

	clf.fit(X,Y)
	
	import pickle
	f = open('%s.model' % __fname__,'wb')
	pickle.dump(clf, f)
	f.close()
	
	
	
	pred = clf.predict(X)
	pred_p = clf.predict_proba(X)[:,1]
	
	print 'AUC:', roc_auc_score(Y, pred_p)
	
	summary.clf_summary(clf, feature_names)
	summary.summary(Y, pred)
	
	
	F1, P, R = TestModel()
	
	#util.notify_me('%s.F1:%.2f,P:%.2f,R:%.2f' % (__fname__, F1*100, P*100, R*100))


