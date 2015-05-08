# coding:utf-8
# find best

import util
import summary
import numpy as np
from sklearn.metrics import f1_score

if __name__=='__main__':
	info = summary.ParTestModelOnData('model16', 'data.test.csv','label_test.csv')
	util.save_obj(info, 'info.info')
	
	pred, Y = info[-2:]
	
	f1scores = {}
	for th in np.linspace(0.3,0.7,20):
		f1score = f1_score(Y, pred>th)
		f1score[str(th)] = f1score
		print th, f1score
	