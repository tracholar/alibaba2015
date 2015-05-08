# coding:utf-8
import numpy as np 
import pandas, sys
import multiprocessing as mp
import util,os
import com 

def FilterDataWithRule(data, rule):
	idx = np.ones(len(data))==1
	if type(rule) is list:
		for r in rule:
			idx &= ~r(data)
	else:
		idx = ~rule(data)
	return data[idx].reset_index(drop=True)  # reset index
	
def RobotRule(data):
	idx = (data['user_click_item_number']>1000) & (data['user_buy_count']==0)
	
	return (idx)

def NouserItem(data):
	idx = (data['item_click_count']==1)&(data['item_added_car']==0)&(data['item_added_start']==0) & (data['item_buy_count']==0)
	idx |= (data['item_click_count']<2) & (data['item_buy_count']==0)
	return (idx)
def UserLeftItem(data):
	idx = (data['user_item_halfmonth_click']==0)&(data['user_item_lastweek_click']==0)&(data['user_item_lastday_add_cart']==0)&(data['user_item_lastday_count']==0) & (data['item_lastweek_click']==0) & (data['item_lastday_count']==0) & (data['item_lastday_add_car']==0) & (data['item_lastweek_add_car']==0)&(data['item_added_car']==0)&(data['item_added_start']==0)& (data['item_buy_count']==0)
	return (idx)
def LastdayRule(data):
	lastday = [i for i in data.keys() if i[:len('user_item_lastday')]=='user_item_lastday']
	last2day = [i for i in data.keys() if i[:len('user_item_last2day')]=='user_item_last2day']
	last3day = [i for i in data.keys() if i[:len('user_item_last3day')]=='user_item_last3day']
	
	
	idx = data[lastday+last2day+last3day].sum(axis=1)==0
	return idx
	
def FilterCSV(fn):
	
	ft = '%s.nofilter.csv' % util.file_basename(fn)
	if not os.path.exists(ft):
		os.rename(fn, ft)
	
	fo = fn
	fn = ft
	
	
	
	block_size = 100000
	reader = pandas.read_csv(fn, iterator=True, chunksize=block_size)
	
	mod = 'w'
	header = True
	i = 0
	
	rules = [LastdayRule]
	for data in reader:
		FilterDataWithRule(data, rules).to_csv(fo, mode=mod, header=header,index=False)
		
		mod = 'a'
		header=False
		
		i = i + len(data)
		print 'process %d rows.' % i 
		
if __name__ == '__main__':
	if sys.argv[1]=='train':
		ff = 'feature.merge.csv'
		fl = 'label.csv'
		fd = 'data.csv'
	elif sys.argv[1]=='test':
		ff = 'feature_test.merge.csv'
		fl = 'label_test.csv'
		fd = 'data.test.csv'
	elif sys.argv[1]=='submit':
		ff = 'feature_total.merge.csv'
	else:
		print __doc__
		sys.exit()
	
	pool = mp.Pool(com.__n_process)
	
	fs = util.FilterFile(util.file_basename(ff).replace('.',r'\.') + r'\.\d+\.csv')
	#print fs
	pool.map(FilterCSV, fs)
		
	
	