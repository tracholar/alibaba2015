# coding:utf-8
'''
用户模型
'''
import sklearn,pandas, pickle, os, summary, util, filter
import numpy as np

from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import f1_score
from sklearn.grid_search import GridSearchCV


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
	
_feature_names = [
	"user_action_count",
	"user_add_star",
	"user_buy_cat_number",
	"user_buy_count",
	"user_buy_item_number",
	"user_geo_f",
	"user_in_hot_pos_2",
	"user_in_hot_pos_5",
	"user_in_hot_pos_6",
	
	"user_lastday_add_cart",
	"user_lastday_add_star",
	"user_lastday_buy",
	"user_lastday_count",
	
	]
def GetFeature(data):

	nolog = ['user_id','item_id', 'buy']

	factor_features = [
		"user_geo_4",
		"user_geo_5",
		"user_geo_9",
		"user_geo_b",
		"user_geo_f",
		"user_geo_i",
		"user_geo_m",
		"user_geo_o",
		"user_geo_t",
		"user_geo_v",
		"user_in_hot_pos_1",
		"user_in_hot_pos_2",
		"user_in_hot_pos_3",
		"user_in_hot_pos_4",
		"user_in_hot_pos_5",
		"user_in_hot_pos_6",
		"user_in_hot_pos_7",
	]
	feature_names = [i for i in _feature_names if i not in nolog and i not in factor_features]
	
	X1 = np.log(0.3+data[feature_names])
	X2 = dict()
	X2['user_convert_rate'] = data['user_buy_count'] / (1+data['user_action_count']+data['user_add_car']*4+data['user_add_star']*4+data['user_buy_count']*10)
	X2 = pandas.DataFrame(X2)
	
	X3 = data[factor_features]
	
	
	X = pandas.concat([X1, X2, X3], axis=1)
	
	
	
	return X[_feature_names]

		
def GetModel():
	
	f = open('%s.model' % __fname__,'rb')
	clf = pickle.load(f)
	f.close()
	return clf

def TestModel():
	summary.TestModel(__fname__)
	
if __name__ == '__main__':
	
	X, Y = GetData()
	
	samples = (np.random.rand(len(Y))<.02) | (Y==1)
	
	print len(samples==1), np.sum(Y==1)
	X, Y = X[samples], Y[samples]
	
	
	feature_names = X.columns
	parms = {
	'C': np.logspace(-1,0,4),  # 
	#'class_weight':[{0:1,1:10}] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	}
	lr = LogisticRegression(penalty='l1')
	clf = GridSearchCV(lr, parms, scoring='f1', n_jobs=10)

	clf.fit(X,Y)
	
	import pickle
	f = open('%s.model' % __fname__,'wb')
	pickle.dump(clf, f)
	f.close()
	
	print __doc__
	
	pred = clf.predict(X)
	
	summary.clf_summary(clf, feature_names)
	summary.summary(Y, pred)
	
	
	TestModel()
	
	util.notify_me('%s is finished' % __fname__)


