# coding:utf-8
'''
对数据集采样
'''

import pandas,sys,csv,com,util
import numpy as np
from com import GetRecItems


def Sample(fn, fo):
	np.random.seed(44)

	block_size = 100000
	reader = pandas.read_csv(fn, iterator=True, chunksize=block_size)

	header = True
	if fn[-6:] == '.0.csv':
		mod = 'w'
	else:
		mod = 'a'
		header = False
		
	train_rows = 0
	train_trows = 0

	rows = 0

	fname1 = fo

	items = GetRecItems()


	for data in reader:
		
		
		
		train = ((data['buy']==1) | (np.random.rand(len(data))<.3)) # 0.045	
		
		
		#print train[:10]
		#print test[:10]
		#print 
		
		
		
			
		data[train].to_csv(fname1, mode=mod, header = header,index = False)

		
		header = False
		mod = 'a'
		
		train_rows = np.sum(train) + train_rows

		train_trows = np.sum(data['buy'][train]==1) + train_trows

		rows = rows + len(data)
		print '[%s] process %d rows!' % (fn,rows)
		# print data.head()
		
	
	
	return (train_rows, train_trows)


if __name__ == '__main__':
	if sys.argv[1]=='train':
		fs = util.FilterFile(r'data\.\d+\.csv')
		train_rows, train_trows = 0,0
		for f in fs:
			i,j = Sample(f, 'data.train.csv')
			train_rows += i 
			train_trows += j
			
		print 'sample %d rows, positive %d rows. ' % (train_rows, train_trows)