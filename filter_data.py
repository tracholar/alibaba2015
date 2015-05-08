# coding:utf-8
'''
filter
'''
import pandas
import numpy as np

import model7 as model 

block_size = 100000
reader = pandas.read_csv('data.csv', iterator=True, chunksize=block_size)

header = True
mod = 'w'
rows = 0
trows = 0 

# clf = model.GetModel()

for data in reader:
	X = model.GetFeature(data)
	idx = (data['user_action_count']>200)  & (data['item_click_count']>5) & (data['user_buy_count'] / (1+data['user_action_count']) > 0.001)
	idx = idx & (data['item_added_car']>=1)
	#Y = clf.predict_proba(X)[:,1]
	#idx = Y>0.01
	
	
	idx = idx | (data['buy']==1)
	# print np.sum(data[idx]['buy']==1)
	data[idx].to_csv('data.filter.csv', mode=mod, header = header,index = False)
	header = False
	mod = 'a'

	rows = rows + len(data)
	print 'process %d rows!' % rows
	
	trows = trows + np.sum(data['buy'][idx])

print 'positive rows', trows