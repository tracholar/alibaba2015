# coding:utf-8
'''
利用特征 最后一天对物品点击数，最后一天对品牌点击数， 用户转化率，商品最后一天热门程度
'''
import sklearn,pandas, pickle, os, summary, util
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
	
def GetFeature(data):

	
	feature_names = [i for i in data.columns if i not in ['user_id','item_id','buy']]
	
	X1 = np.log(0.3+data[feature_names])
	X2 = dict()
	X2['user_convert_rate'] = data['user_buy_count'] / (1+data['user_action_count'])
	X2['item_convert_rate'] = data['item_buy_count'] / (1+data['item_click_count'])
	X2 = pandas.DataFrame(X2)
	
	X = pandas.concat([X1, X2], axis=1)
	
	feature_names = [
		"user_action_count",
		"user_lastday_count",
		"user_buy_count",
		"item_click_count",
		"item_lastday_count",
		"item_buy_count",
		"cat_click_count",
		"cat_buy_count",
		"user_cat_count",
		"user_cat_lastday_count",
		"user_item_count",
		"user_item_lastday_count",
		"user_add_car",
		"user_add_star",
		"item_added_car",
		"item_added_start",
		"user_item_lasttime",
		"cat_add_car",
		"cat_add_star",
		"user_item_buy",
		"user_item_before_halfmonth_click",
		"user_item_before_halfmonth_star",
		"user_item_before_halfmonth_add_car",
		"user_item_before_halfmonth_buy",
		"user_cat_halfmonth_star",
		"user_cat_before_halfmonth_click",
		"user_cat_before_halfmonth_star",
		"user_cat_before_halfmonth_add_car",
		"user_cat_before_halfmonth_buy",
		"user_lastday_add_star",
		"user_item_lastday_add_star",
		"user_cat_lastday_add_star",
		"user_lastday_add_cart",
		"user_item_lastday_add_cart",
		"user_cat_lastday_add_cart",
		"user_lastday_buy",
		"user_item_lastday_buy",
		"user_cat_lastday_buy",
		"item_convert_rate",
		"user_convert_rate",
		]
	return X[feature_names]

		
def GetModel():
	
	f = open('%s.model' % __fname__,'rb')
	clf = pickle.load(f)
	f.close()
	return clf

def TestModel():
	summary.TestModel(__fname__)
	
if __name__ == '__main__':
	
	X, Y = GetData()

	feature_names = X.columns
	parms = {
	'C': np.logspace(-2.5,1,10),  # 0.5是最好的
	#'class_weight':[{0:1,1:r} for r in np.logspace(0,2,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	}
	lr = LogisticRegression(penalty='l1')
	clf = GridSearchCV(lr, parms, scoring='f1', n_jobs=10)

	clf.fit(X,Y)
	
	import pickle
	f = open('%s.model' % __fname__,'wb')
	pickle.dump(clf, f)
	f.close()
	
	
	
	pred = clf.predict(X)
	
	summary.clf_summary(clf, feature_names)
	summary.summary(Y, pred)
	
	
	TestModel()
	
	util.notify_me('%s is finished' % __fname__)


