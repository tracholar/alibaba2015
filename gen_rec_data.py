# coding:utf-8
# rec for user item
'''
usage gen_rec_data.py modelname
for example
python gen_rec_data.py model0

'''
import sklearn,pandas,csv,sys
import numpy as np

from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import f1_score

import pickle,sys, util,com
import multiprocessing as mp




def GenRecDataFromFeatureFile(args):
	modelname, fn = args
	#th = 0.58
	
	# load model
	model = util.load_model_from_name(modelname)

	clf = model.GetModel()
	
	items = pandas.read_csv('tianchi_mobile_recommend_train_item.csv')
	items = set(items['item_id'])
	
	

	block_size = 10000
	fr = pandas.read_csv(fn, iterator=True, chunksize=block_size)
	rec_set = set()
	
	
	i = 0
	for data in fr:
		
		X = model.GetFeature(data)
		
		#if th is not None:
		#	Y = clf.predict_proba(X)[:,1] > th
		#else:
		#	Y = clf.predict(X)
		
		Y = clf.predict(X)
		
		
		for idx in range(len(data)):
			uid = data['user_id'][idx]
			tid = data['item_id'][idx]
			if tid in items and Y[idx]==1:
				print uid,tid
				
				rec_set.add((uid, tid))
		i = i + block_size
		
		print 'processed %d row!' % i
	return rec_set
if __name__ == '__main__':
	if len(sys.argv)!=2:
		print __doc__
		sys.exit()

	fout = 'submit.%s.csv' % sys.argv[1]



	# load need to be recommanded item
	



	fo = open(fout, 'wb')
	fw = csv.writer(fo, delimiter=',')
	fw.writerow(['user_id','item_id'])

	rec_set =  set()

	pool = mp.Pool(com.__n_process)

	re_str = r'feature_total\.merge\.\d+\.csv$'
	f_list = util.FilterFile(re_str)
	rec_set_list = pool.map(GenRecDataFromFeatureFile,[(sys.argv[1], f) for f in f_list])

	for r in rec_set_list:
		rec_set |= r 

	for uid, tid in rec_set:
		fw.writerow([uid, tid])
	fo.close()
	
	nrows = len(rec_set)
	print 'recommand %d record.' % nrows
	util.notify_me('recommand data are done! %d record.' % nrows)