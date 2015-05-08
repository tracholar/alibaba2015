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
	
_feature_names = [
	"user_action_count",
	"user_lastday_count",
	"user_buy_count",
	"item_click_count",
	"item_lastday_count",
	"item_buy_count",
	"cat_click_count",
	"cat_buy_count",
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
	"user_item_click_nobuy",
	"user_item_cart_nobuy",
	"user_item_buy_again",
	"user_geo_f",
	"user_geo_m",
	"user_geo_9",
	"user_cat_aveThreeDayDelta_click",
	"user_cat_aveThreeDayDelta_add_car",
	"user_cat_aveThreeDayDelta_buy",
	"user_item_aveThreeDayDelta_click",
	"user_item_aveThreeDayDelta_star",
	"user_item_aveThreeDayDelta_add_car",
	"user_item_aveThreeDayDelta_buy",


	]
def GetFeature(data):

	nolog = ['user_id','item_id', 'buy']
	nolog2 = ['user_cat_aveThreeDayDelta_click','user_cat_aveThreeDayDelta_star','user_cat_aveThreeDayDelta_add_car','user_cat_aveThreeDayDelta_buy','user_item_aveThreeDayDelta_click','user_item_aveThreeDayDelta_star','user_item_aveThreeDayDelta_add_car','user_item_aveThreeDayDelta_buy']
	factor_features = [
		"user_item_click_nobuy",
		"user_item_star_nobuy",
		"user_item_cart_nobuy",
		"user_item_buy_again",
		"user_geo_b","user_geo_f","user_geo_i","user_geo_m","user_geo_o","user_geo_5","user_geo_4","user_geo_v","user_geo_9","user_geo_t",
		"item_geo_9","item_geo_4","item_geo_m","item_geo_t","item_geo_f",
	]
	feature_names = [i for i in data.columns if i not in nolog and i not in factor_features and i not in nolog2]
	
	X1 = np.log(0.3+data[feature_names])
	X2 = dict()
	X2['user_convert_rate'] = data['user_buy_count'] / (1+data['user_action_count'])
	X2['item_convert_rate'] = data['item_buy_count'] / (1+data['item_click_count'])
	X2 = pandas.DataFrame(X2)
	
	X3 = data[factor_features]
	
	feature_names2= [i for i in data.columns if i in nolog2]
	
	X4 = np.copysign(np.log(0.3+np.abs(data[feature_names2])),np.sign(data[feature_names2]))
	
	X = pandas.concat([X1, X2, X3, X4], axis=1)
	
	
	
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

	feature_names = X.columns
	parms = {
	'C': np.logspace(-2,2,10),  # 
	#'class_weight':[{0:1,1:r} for r in np.linspace(1,3,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
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
	
	
	F1, P, R = TestModel()
	
	util.notify_me('%s.F1:%.2f,P:%.2f,R:%.2f' % (__fname__, F1*100, P*100, R*100))


