# coding:utf-8
'''
物品模型
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
	"cat_add_car",
"cat_before_halfmonth_buy",
"cat_before_halfmonth_click",
"cat_before_halfmonth_star",
"cat_buy_count",
"cat_buy_user_number",
"cat_click_count",
"cat_halfmonth_buy",
"cat_halfmonth_click",
"cat_halfmonth_star",
"cat_lastday_add_car",
"cat_lastday_buy",
"cat_lastday_buy_again",
"cat_lastday_cart_nobuy",
"cat_lastday_click",
"cat_lastday_click_nobuy",
"cat_lastday_star",
"cat_lastday_star_nobuy",
"cat_lastweek_add_car",
"cat_lastweek_click",
"cat_lastweek_star",
"geo_users_number",
"geo_users_number",
"item_added_car",
"item_added_start",
"item_before_halfmonth_add_car",
"item_before_halfmonth_buy",
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
"item_lastday_buy_again",
"item_lastday_cart_nobuy",
"item_lastday_click",
"item_lastday_click_nobuy",
"item_lastday_count",
"item_lastday_star_nobuy",
"item_lastweek_add_car",
"item_lastweek_buy",
"item_lastweek_click",
"item_lastweek_star",
"geo_users_number",
"item_share_major",



]

def GetFeature(data):


	
	data['item_share_major'] = (data['item_buy_count']/(1+data['cat_buy_count']))>.2
	
	nolog = ['user_id','item_id', 'buy']
	

	factor_features = [
		"item_share_major",
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
"geo_users_number",
	]
	
	
	
	
	
	X1 = np.log(.3+data[log_features])
	X2 = data[factor_features]
	
	X = pandas.concat([X1, X2], axis=1)
	
	
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


	samples = (np.random.rand(len(Y))<0.5) | (Y==1)
	X = X[samples]
	Y = Y[samples]
	
	feature_names = X.columns
	parms = {
	'C': [1.], #np.logspace(-2,2,5),  # 
	#'lr__class_weight':[{0:1,1:.95}],#[{0:1,1:r} for r in np.linspace(1,3,10)] #[{0:1,1:50},{0:1,1:70},{0:1,1:85},{0:1,1:100},{0:1,1:120},{0:1,1:150}]
	#'lda__n_components':[50,60],
	}
	tr = StandardScaler()
	#lda = PCA(n_components=40)
	lr = LogisticRegression(penalty='l1')
	#pipe = Pipeline([('tr',tr),('lr',lr)])
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


