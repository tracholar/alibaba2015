# coding:utf-8
# merge.py
# usage  python merge.py file1 file2
import csv, sys, pandas
import numpy as np

if len(sys.argv)<4:
	print 'usage  python merge.py file1 file2 ... file_out'
	
	
block_size = 100000
r1 = pandas.read_csv(sys.argv[1], iterator=True, chunksize=block_size)
r2 = pandas.read_csv(sys.argv[2], iterator=True, chunksize=block_size)

mod = 'w'
header = True

nrows = 0
for df1 in r1:
	df2 = r2.get_chunk()
	if len(df1)!= len(df2):
		print 'data error'
		sys.exit()
	if np.sum(np.sum(df1[['user_id', 'item_id']] == df2[['user_id', 'item_id']]))!=2*len(df1):
		print 'key error'
		
		for i in range(len(df1)):
			if not ((df1['user_id'][i] == df2['user_id'][i]) and (df1['item_id'][i] == df2['item_id'][i])):
				print '%dth row dismatch.' % (i+1)
		
		sys.exit()
	df = pandas.concat([df1, df2[[field for field in df2.keys() if field not in ['user_id', 'item_id']]]], axis=1)
	df.to_csv(sys.argv[3], mode=mod, header = header,index = False)
	header = False
	mod = 'a'

	nrows = nrows + block_size
	print 'processed %d rows!' % nrows




