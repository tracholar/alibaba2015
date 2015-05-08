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
	

_feature_names = [
	
	#"user_item_cart_nobuy",
	#"user_item_buy_again",
	
	"user_item_lastday_cart_nobuy",
	# "user_item_count",
# #	"user_item_buy",  # 没有user_item_buy_agin好用
	"user_item_buy_again",
	# "user_item_lastday_add_star",
	# "user_item_lastday_buy",
	
	# "user_item_lastweek_add_car",
	# "user_item_lastweek_buy",
	# "user_item_lastweek_click",
	# "user_item_lastweek_star",
	
	# "user_item_last14day_buy",
	# "user_item_last21day_buy",
	# "user_item_last2day_add_car",
	# "user_item_last2day_buy",
	# "user_item_last2day_click",
	# "user_item_last2day_star",
	# "user_item_last3day_add_car",
	# "user_item_last3day_buy",
	# "user_item_last3day_click",
	# "user_item_last3day_star",
	# "user_item_last7day_buy",
	
	# "user_item_lastday_add_cart",
	# "user_item_lastday_count",
	

	
	# "user_cat_buy",
	

	
	# "user_convert_rate",
	# "user_lastday_count",
	# "user_lastday_add_cart",
	# "user_is_robot",
	# "user_geo_9",
	# "user_in_hot_pos_4",
	# "user_action_count",
	# "user_add_car",
	# "user_add_star",
	# "user_buy_cat_number",
	# "user_buy_count",
	# "user_buy_item_number",

	
	# "item_convert_rate",
	# "item_buy_count",
	# "item_lastday_count",
#	"user_item_lastday_click_nobuy",
	
	
#	"user_item_lastday_count",
#	"user_item_lastday_buy",
	
	"user_item_last2day_cart_nobuy",
	"user_item_last3day_cart_nobuy",
		
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
#	"user_item_buy",
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
#	"user_lastday_add_cart",  # 用 user_lastday_add_cartnobuy
	"user_item_lastday_add_cart",
	"user_cat_lastday_add_cart",
	"user_lastday_buy",
	"user_item_lastday_buy",
	"user_geo_f",
	"user_geo_m",
	"user_geo_o",
	"user_geo_9",
	"user_geo_t",
	"user_item_star_nobuy",
	"user_item_cart_nobuy",
	"user_item_buy_again",
	"user_cat_aveThreeDayDelta_click",
	"user_cat_aveThreeDayDelta_star",
	"user_cat_aveThreeDayDelta_add_car",
	"user_cat_aveThreeDayDelta_buy",
	"user_item_aveThreeDayDelta_click",
	"user_item_aveThreeDayDelta_star",
	"user_item_aveThreeDayDelta_add_car",
	 
	
]
_feature_names = [  #list(set(_feature_names))
"cat_add_car",
"cat_add_star",
"cat_before_halfmonth_add_car",
"cat_before_halfmonth_buy",
"cat_before_halfmonth_click",
"cat_before_halfmonth_star",
"cat_buy_count",
"cat_halfmonth_add_car",
"cat_halfmonth_click",
"cat_halfmonth_star",
"cat_lastday_add_car",
"cat_lastday_buy",
"cat_lastday_click",
"cat_lastday_star",
"cat_lastweek_add_car",
"cat_lastweek_buy",
"cat_lastweek_click",
"cat_lastweek_star",
"geo_users_number",
"item_added_car",
"item_added_start",
"item_before_halfmonth_click",
"item_buy_count",
"item_buy_user_number",
"item_click_count",
"item_halfmonth_add_car",
"item_halfmonth_buy",
"item_halfmonth_click",
"item_halfmonth_star",
"item_lastday_add_car",
"item_lastday_buy",
"item_lastday_click",
"item_lastday_count",
"item_lastday_star",
"item_lastweek_add_car",
"item_lastweek_buy",
"item_lastweek_click",
"user_action_count",
"user_add_car",
"user_add_star",
"user_buy_cat_number",
"user_buy_count",
"user_buy_item_number",
"user_cat_before_halfmonth_add_car",
"user_cat_before_halfmonth_buy",
"user_cat_before_halfmonth_click",
"user_cat_count",
"user_cat_halfmonth_add_car",
"user_cat_halfmonth_click",
"user_cat_halfmonth_star",
"user_cat_lastday_add_cart",
"user_cat_lastday_add_star",
"user_cat_lastday_buy",
"user_cat_lastday_count",
"user_cat_lastweek_add_car",
"user_cat_lastweek_buy",
"user_cat_lastweek_click",
"user_cat_lastweek_star",
"user_item_1212_buy",
"user_item_1212_click",
"user_item_before_halfmonth_add_car",
"user_item_before_halfmonth_buy",
"user_item_before_halfmonth_click",
"user_item_buy",
"user_item_count",
"user_item_halfmonth_add_car",
"user_item_halfmonth_buy",
"user_item_halfmonth_click",
"user_item_halfmonth_star",
"user_item_last14day_buy",
"user_item_last2day_add_car",
"user_item_last2day_buy",
"user_item_last2day_click",
"user_item_last2day_star",
"user_item_last3day_click",
"user_item_lastday_add_cart",
"user_item_lastday_count",
"user_item_lasttime",
"user_item_lastweek_add_car",
"user_item_lastweek_click",
"user_item_lastweek_star",
"user_lastday_add_cart",
"user_lastday_add_star",
"user_lastday_buy",
"user_lastday_count",
"usergeo_item_before_lastday_cart",
"usergeo_item_before_lastday_click",
"usergeo_item_lastday_cart",
"user_active_days",
"item_active_days",
"cat_active_days",
"item_lastweek_active_days",
"cat_lastweek_active_days",
"user_item_active_days",
"user_item_lastweek_active_days",
"user_cat_active_days",
"user_lastday_active_hours",
"item_lastday_active_hours",
"cat_lastday_active_hours",
"user_last_active_time",
"item_last_active_time",
"cat_last_active_time",
"user_cat_last_active_time",
"cat_lastday_buy_again",
"cat_lastday_cart_nobuy",
"cat_lastday_star_nobuy",
"user_cat_lastday_buy_again",
"user_cat_lastday_cart_nobuy",
"user_cat_lastday_click_nobuy",
"user_geo_9",
"user_geo_m",
"user_in_hot_pos_2",
"user_in_hot_pos_3",
"user_in_hot_pos_4",
"user_in_hot_pos_5",
"user_in_hot_pos_7",
"user_item_cart_nobuy",
"user_item_click_nobuy",
"user_item_lastday_cart_nobuy",
"user_item_star_nobuy",
"user_item_last2day_cart_nobuy",
"user_die",
"user_cat_aveThreeDayDelta_buy",
"user_cat_aveThreeDayDelta_click",
"user_item_aveThreeDayDelta_add_car",
"user_item_aveThreeDayDelta_buy",
"user_item_aveThreeDayDelta_click",
"user_item_aveThreeDayDelta_star",
"user_item_geo_distance",


]
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
	'C': [.09], #np.logspace(-2,2,5),  # 
	#'class_weight': [{0:1,1:r} for r in np.linspace(1,10,10)]
	'class_weight':[{0:1,1:1.1}],#[{0:1,1:r} for r in np.linspace(1,3,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	#'lda__n_components':[50,60],
	}
	tr = StandardScaler()
	#lda = PCA(n_components=40)
	lr = LogisticRegression(penalty='l1')
	pipe = Pipeline([('tr',tr),('lr',lr)])
	clf = GridSearchCV(lr, parms, scoring='f1', n_jobs=1)

	
	
	

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


