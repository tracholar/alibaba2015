# coding:utf-8
'''
基于模型16，增加交叉特则
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
import model11

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
"item_buy_count",
"cat_click_count",
"cat_buy_count",
"user_cat_lastday_count",
"user_item_count",
"user_add_car",
"user_add_star",
"user_item_buy",
"user_item_before_halfmonth_click",
"user_cat_before_halfmonth_click",
"user_cat_before_halfmonth_buy",
"user_lastday_add_star",
"user_item_lastday_add_star",
"user_cat_lastday_add_star",
"user_lastday_buy",
"user_item_cart_nobuy",
"user_cat_aveThreeDayDelta_click",
"user_cat_aveThreeDayDelta_add_car",
"user_cat_aveThreeDayDelta_buy",
"user_item_aveThreeDayDelta_click",
"user_item_aveThreeDayDelta_add_car",
"geo_users_number",
"user_item_lastday_click_nobuy",
"user_item_lastday_cart_nobuy",
"user_cat_lastday_cart_nobuy",
"item_lastday_click",
"item_lastday_buy",
"item_lastweek_click",
"item_halfmonth_click",
"item_before_halfmonth_click",
"item_before_halfmonth_add_car",
"user_buy_cat_number",
"cat_buy_user_number"
]
def GetFeature(data):


	
	data['item_share_major'] = (data['item_buy_count']/(1+data['cat_buy_count']))>.2
	data['user_die'] = ((data['user_lastday_count'])<3)
	
	nolog = ['user_id','item_id', 'buy']
	

	factor_features = [
		
		
"cat_lastday_buy_again",
"cat_lastday_cart_nobuy",
"cat_lastday_click_nobuy",
"cat_lastday_star_nobuy",
"item_geo_4",
"item_geo_9",
"item_geo_f",
"item_geo_m",
"item_geo_t",
"item_lastday_buy_again",
"item_lastday_cart_nobuy",
"item_lastday_click_nobuy",
"item_lastday_star_nobuy",
"user_cat_lastday_buy_again",
"user_cat_lastday_cart_nobuy",
"user_cat_lastday_click_nobuy",
"user_cat_lastday_star_nobuy",
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
"user_item_buy_again",
"user_item_cart_nobuy",
"user_item_click_nobuy",
"user_item_lastday_buy_again",
"user_item_lastday_cart_nobuy",
"user_item_lastday_click_nobuy",
"user_item_lastday_star_nobuy",
"user_item_star_nobuy",


	]
	
	signed_log_features = [
		"user_cat_aveThreeDayDelta_add_car",
"user_cat_aveThreeDayDelta_buy",
"user_cat_aveThreeDayDelta_click",
"user_cat_aveThreeDayDelta_star",

"user_item_aveThreeDayDelta_add_car",
"user_item_aveThreeDayDelta_buy",
"user_item_aveThreeDayDelta_click",
"user_item_aveThreeDayDelta_star",

	]
	
	log_features = [
		
	"cat_add_car",
"cat_add_star",
"cat_before_halfmonth_add_car",
"cat_before_halfmonth_buy",
"cat_before_halfmonth_click",
"cat_before_halfmonth_star",
"cat_buy_count",
"cat_buy_user_number",
"cat_click_count",
"cat_halfmonth_add_car",
"cat_halfmonth_buy",
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
"item_before_halfmonth_add_car",
"item_before_halfmonth_buy",
"item_before_halfmonth_click",
"item_before_halfmonth_star",
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
"item_lastweek_star",
"user_action_count",
"user_add_car",
"user_add_star",
"user_buy_cat_number",
"user_buy_count",
"user_buy_item_number",

"user_cat_before_halfmonth_add_car",
"user_cat_before_halfmonth_buy",
"user_cat_before_halfmonth_click",
"user_cat_before_halfmonth_star",
"user_cat_count",
"user_cat_halfmonth_add_car",
"user_cat_halfmonth_buy",
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
"user_item_before_halfmonth_add_car",
"user_item_before_halfmonth_buy",
"user_item_before_halfmonth_click",
"user_item_before_halfmonth_star",
"user_item_buy",

"user_item_count",

"user_item_halfmonth_add_car",
"user_item_halfmonth_buy",
"user_item_halfmonth_click",
"user_item_halfmonth_star",
"user_item_lastday_add_cart",
"user_item_lastday_add_star",
"user_item_lastday_buy",
"user_item_lastday_count",
"user_item_lasttime",
"user_item_lastweek_add_car",
"user_item_lastweek_buy",
"user_item_lastweek_click",
"user_item_lastweek_star",

"user_lastday_add_cart",
"user_lastday_add_star",
"user_lastday_buy",
"user_lastday_count",
"usergeo_item_before_lastday_buy",
"usergeo_item_before_lastday_cart",
"usergeo_item_before_lastday_click",
"usergeo_item_before_lastday_star",
"usergeo_item_lastday_buy",
"usergeo_item_lastday_cart",
"usergeo_item_lastday_click",
"usergeo_item_lastday_star",
	]
	
	linear_features = [
		"user_item_geo_distance",
	]
	X1 = np.log(.3+data[log_features])
	X2 = data[factor_features]
	X3 = data[linear_features]
	X4 = np.copysign(np.log(.3+np.abs(data[signed_log_features])),np.sign(data[signed_log_features]))
	
	X = pandas.concat([X1, X2,X3, X4], axis=1)
	
	
	# transformer = sklearn.preprocessing.MinMaxScaler()
	# X = transformer.fit_transform(X[_feature_names])
	#poly = PolynomialFeatures(include_bias=False, interaction_only=True)
	#X = poly.fit_transform(X[_feature_names])
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


	samples = np.random.rand(len(Y))<0.5
	X = X[samples]
	Y = Y[samples]
	
	feature_names = X.columns
	parms = {
	'lr__C': [1],#np.logspace(-2,2,5),  # 
	#'lr__class_weight':[{0:1,1:.95}],#[{0:1,1:r} for r in np.linspace(1,3,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	#'lda__n_components':[50,60],
	}
	tr = StandardScaler()
	pca = PCA(n_components=10)
	lr = LinearSVC(penalty='l1',dual=False)
	pipe = Pipeline([('tr',tr),('pca',pca),('lr',lr)])
	clf = GridSearchCV(pipe, parms, scoring='f1', n_jobs=5)

	
	
	

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


