# coding:utf-8
'''
usage: select_feature.py model0
'''
import sys,util
import numpy as np

if len(sys.argv)!=2:
	print __doc__
model = util.load_model_from_name(sys.argv[1])
clf = model.GetModel()
X,Y = model.GetData()
feature_names = X.keys()

eps = 1e-6
if hasattr(clf.best_estimator_,'named_steps'):
	if 'lr' in clf.best_estimator_.named_steps:
		est = clf.best_estimator_.named_steps['lr']
	else:
		est = clf.best_estimator_
else:
	est = clf.best_estimator_

for i in range(len(feature_names)):
	if np.abs(est.coef_[0][i])>=eps:
		print '"%s",\n' % feature_names[i],
print '\n'

for i in range(len(feature_names)):
	if np.abs(est.coef_[0][i])<eps:
		print '"%s",\n' % feature_names[i],
		
