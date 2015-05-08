# coding:utf-8
import multiprocessing as mp
import numpy as np
import pandas as pd

import sys

def f(args):
	
	
	data = reader.get_chunk()
	
	
	rec_set = set()
	
	#l.acquire()
	
	#l.release()
	
	
	for i in range(len(data)):
		#print data['buy'][i]
		if data['buy'][i] == 1:
			
			rec_set.add((data['user_id'][i], data['item_id'][i]))
	
	return rec_set
	
	
	
if __name__ == '__main__':
	
	q = mp.Queue()
	pool = mp.Pool(20)
	l = mp.Lock()
	
	reader = pd.read_csv('data.csv', iterator=True, chunksize=10000)
	
	q.put(reader)
	
	# map 
	set_list = pool.map(f, [q for i in range(20)])
	
	# reduce
	rec_set = set()
	for s in set_list:
		rec_set |= s 
	
	print len(rec_set)
	
	