# coding:utf-8
'''
usage summary.py modelname
'''
	
	
import sklearn,pandas
from sklearn.metrics import f1_score,precision_score,recall_score,confusion_matrix, roc_auc_score
from sklearn.linear_model import  LogisticRegression
import numpy as np 
import util, sys , com, time
import multiprocessing as mp
from sklearn.grid_search import GridSearchCV

def summary(Y, pred):
	
	print 'F1\tP\tR'
	print '%.2f\t%.2f\t%.2f' % (f1_score(Y, pred)*100, precision_score(Y,pred)*100, recall_score(Y, pred)*100)
	
	print ''
	print ' \tF\tT'
	print 'N\t%d\t%d' % (np.sum((Y==0) & (pred==0)), np.sum((Y==0) & (pred==1)))
	print 'P\t%d\t%d' % (np.sum((Y==1) & (pred==0)), np.sum((Y==1) & (pred==1)))
	print '\n'
	

def estimator_coef(clf, feature_names=None):
	print 'clf parms (%d features):' % len(clf.coef_[0])
	if feature_names is None or len(feature_names)!=len(clf.coef_[0]):
		print clf.intercept_[0],
		for c in clf.coef_[0]:
			print c,
		print '\n'
	else:
		print 'intercept\t%.6f' % clf.intercept_[0]
		for i in range(len(clf.coef_[0])):
			print '%s\t%.6f' % (feature_names[i],clf.coef_[0][i])
		print '\n'

	
def clf_summary(clf, feature_names=None):
	# print clf
	
	if isinstance(clf, GridSearchCV):
		print 'best score', clf.best_score_
		print 'best parms', clf.best_params_
	
	if not hasattr(clf, 'best_estimator_'):
		setattr(clf, 'best_estimator_', clf)
		
	if hasattr(clf.best_estimator_,'named_steps'):
		if 'lr' in clf.best_estimator_.named_steps:
			est = clf.best_estimator_.named_steps['lr']
		else:
			est = clf.best_estimator_
	else:
		est = clf.best_estimator_
		
	if not isinstance(est, LogisticRegression):
		print est
		return
	
	
	estimator_coef(est, feature_names)
	
def _ParTestModelOnData(args):
	modelname, fdata = args
	m = util.load_model_from_name(modelname)
	
	clf = m.GetModel()
	block_size = 10000
	reader = pandas.read_csv(fdata, iterator=True, chunksize=block_size)
	rec_set = set()
	
	pred_prob = np.array([])
	Y_true = np.array([])
	
	for data in reader:
		
		X_test = m.GetFeature(data)
		Y_test = data['buy']
	
	
		pred_p = clf.predict_proba(X_test)[:,1]
		#pred = clf.predict(X_test)

		pred_prob = np.concatenate([pred_prob, pred_p])
		Y_true = np.concatenate([Y_true, Y_test])
		
		# auc
		
		for i in range(len(data)):
			if pred_p[i]>.5:
				rec_set.add((data['user_id'][i], data['item_id'][i]))
		
	return rec_set, pred_prob, Y_true
	
def ParTestModelOnData(modelname, fdata, flabel):
	
	block_size = 10000
	
	rec_set = set()
	actual_set = com.GetBuySet(flabel)

	f_base = util.file_basename(fdata)
	
	re_str = f_base.replace('.',r'\.') + r'\.\d+\.csv$'
	f_list = util.FilterFile(re_str) #['%s.%d.csv' % (f_base, j) for j in range(com.__n_process)]
	
	pool = mp.Pool(com.__n_process)
	rec_set_list = pool.map(_ParTestModelOnData, [(modelname, f) for f in f_list])
	
	pred_prob = np.array([])
	Y_true = np.array([])
	for r,p,y in rec_set_list:
		rec_set |= r
		pred_prob = np.concatenate([pred_prob,p])
		Y_true = np.concatenate([Y_true, y])
		
	TP = len(rec_set & actual_set)
	TN = len(rec_set - actual_set)
	FP = len(actual_set - rec_set)
	
	PrintConfuseMatrix(TP, TN, FP)
	P, R, F1 =  GetPRF1(TP, TN, FP)
	PrintPRF1(P, R, F1)
	

	
	print 'AUC:', roc_auc_score( Y_true.astype(int),  pred_prob)
	
	
	return TP, TN, FP, P, R, F1, pred_prob,Y_true
	
	
def TestModelOnData(modelname, fdata, flabel):
	actual_set = com.GetBuySet(flabel)
	rec_set = set()
	
	f_base = util.file_basename(fdata)
	
	re_str = f_base.replace('.',r'\.') + r'\.\d+\.csv$'
	f_list = util.FilterFile(re_str) #['%s.%d.csv' % (f_base, j) for j in range(com.__n_process)]
	

	for f in f_list:
		r , p, y = _ParTestModelOnData((modelname, f))
		
		rec_set |= r
		pred_prob = np.concatenate([pred_prob,p])
		Y_true = np.concatenate([Y_true, y])
		
	
	TP = len(rec_set & actual_set)
	TN = len(rec_set - actual_set)
	FP = len(actual_set - rec_set)
	
	PrintConfuseMatrix(TP, TN, FP)
	P, R, F1 =  GetPRF1(TP, TN, FP)
	PrintPRF1(P, R, F1)
	
	print 'AUC:', roc_auc_score( Y_true.astype(int),  pred_prob)
	
	
	return TP, TN, FP, P, R, F1, pred_prob,Y_true
	
def PrintConfuseMatrix(TP, TN, FP, FN='--'):
	print ' \tF\tT'
	print 'N\t%s\t%d' % (FN, TN)
	print 'P\t%d\t%d' % (FP, TP)
	print ''
	
def GetPRF1(TP, TN, FP):
	P = 1.0*TP/(TP + TN)
	R = 1.0*TP/(TP + FP)
	
	F1 = 2*P*R/(P+R)
	return P, R, F1
	
def PrintPRF1(P, R, F1):
	print 'F1\tP\tR'
	print '%.2f\t%.2f\t%.2f' % (F1*100, P*100, R*100)
	
def TestModel(modelname, par=True):
	#model = util.load_model_from_name(modelname)
	#clf = model.GetModel()
	
	c = time.clock()
	if par:
		TestFun = ParTestModelOnData
	else:
		TestFun = TestModelOnData
	print '===== for train ====='
	TestFun(modelname, 'data.csv', 'label.csv')
	print 'cost %s seconds.' % (time.clock() - c)
	
	c = time.clock()
	print '===== for test ====='
	TP, TN, FP, P, R, F1, pred_prob,Y_true = TestFun(modelname, 'data.test.csv', 'label_test.csv')
	print 'cost %s seconds.' % (time.clock() - c)
	# print clf.grid_scores_
	# return TP,TN,FP,FN
	
	print ''
	
	#print '===== for online test ====='
	#TestModelOnData(model, 'data.onlinetest.csv', 'label.onlinetest.csv')
	
	#print '===== for all of data ====='
	#TestModelOnData(model, 'data.csv', 'label.csv')
	
		
	return F1,P,R
	
def SelectFeature(clf, feature_names):
	for i in range(len(feature_names)):
		if np.abs(clf.best_estimator_.coef_[0][i])>1e-4:
			print '"%s",\n' % feature_names[i],

			
if __name__ == '__main__':
	
	
	
	if len(sys.argv)<2:
		print __doc__
		sys.exit()
	model = util.load_model_from_name(sys.argv[1])
	clf = model.GetModel()
	X,Y = model.GetData()
	pred = clf.predict(X)
	pred_prob = clf.predict_proba(X)[:,1]
	
	print 'AUC: %f' % roc_auc_score(Y, pred_prob)
	
	feature_names = X.columns
	
	clf_summary(clf, feature_names)
	print '\n'
	summary(Y,pred)
	
	
	TestModel( sys.argv[1], par=True)