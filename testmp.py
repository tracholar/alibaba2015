# coding:utf-8
'''
test multiprocess for read data
'''
import multiprocessing as mp
import numpy as np
import pandas, util

blocksize = 10000

def Fun(data,id):
	
	model = util.load_model_from_name('model10')
	clf = model.GetModel()
	
	rec_set = []
	X_test = model.GetFeature(data).as_matrix()
	Y_test = data['buy'].as_matrix()
	pred = clf.predict(X_test)
	#print np.sum(Y_test==pred)
	for i in range(len(data)):
		if pred[i]==1:
			rec_set.append((data['user_id'][i], data['item_id'][i]))
	
	print '%s. done!' % id
	return rec_set
	
if __name__ == '__main__':
	
	rec_set = []
	pool = mp.Pool(20)
	block_size = 10000
	reader = pandas.read_csv('data.csv', iterator=True, chunksize=block_size)

	fs = []
	for data in reader:
		f = pool.apply_async(Fun,[data, len(fs)])
		fs.append(f)
		print len(fs)
	
	#print header
	for f in fs:
		rec_set += f.get(100)
		print len(rec_set)
	print len(rec_set)