# coding:utf-8
'''

特征生成文件
测试一个新的想法
为每一天生成一张特征列表

'''
import csv, time,sys, util,com
import numpy as np

from optparse import OptionParser


def IncDict(d, key):
	if key in d:
		d[key] = d[key] + 1
	else:
		d[key] = 1
def AppendDict(d,key,val):
	if key not in d:
		d[key] = set()
	
	d[key].add(val)
	
def GetDict(d, key, f=lambda x:x):
	if key in d:
		return f(d[key])
	else:
		return 0

def DiffTime(t1, t2):
	t1 = time.mktime(time.strptime(t1,'%Y-%m-%d %H'))
	t2 = time.mktime(time.strptime(t2,'%Y-%m-%d %H'))
	return t1 - t2
def GetHours(t): # 距离7月1日0点的小时数
	m = int(t[5:7])
	d = int(t[8:10])
	h = int(t[11:])
	return ((m-7)*31+d-1)*24+h 
def DiffHours(t1, t2):
	return GetHours(t1) - GetHours(t2)
	
	
def GenFeature(finput='user_action_train.csv', foutput = 'feature.csv', day='2014-12-18', lastday = '2014-12-18'):
	

	
	
	# 细化行为特征
	# 用户买的物品数目
	#
	
	user_active_hours = dict()
	item_active_hours = dict()
	cat_active_hours = dict()
	
	user_item_active_hours = dict()
	user_cat_active_hours = dict()
	
	user_click_count = dict()
	user_star_count = dict()
	user_add_cart_count = dict()
	user_buy_count = dict()
	
	user_buy_items = dict()
	user_buy_cats = dict()
	user_click_items = dict()
	user_click_cats = dict()
	user_star_items = dict()
	user_star_cats = dict()
	user_add_cart_items = dict()
	user_add_cart_cats = dict()
	
	item_click_count = dict()
	item_star_count = dict()
	item_add_cart_count = dict()
	item_buy_count = dict()
	
	cat_click_count = dict()
	cat_star_count = dict()
	cat_add_cart_count = dict()
	cat_buy_count = dict()
	
	user_item_click_count = dict()
	user_item_star_count = dict()
	user_item_add_cart_count = dict()
	user_item_buy_count = dict()
	
	
	user_cat_click_count = dict()
	user_cat_star_count = dict()
	user_cat_add_cart_count = dict()
	user_cat_buy_count = dict()
	
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()

	with open(finput, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		header = reader.next()
		print header
		
		last7day = util.LastNDay(lastday,7)[:10]
		
		i = 0
		for row in reader:
			#if row[5] > '%s 23' % lastday : # 未来的数据
			#	continue
			
			
			uid = row[0]
			tid = row[1]
			cid = row[4]
			t = row[5]
			h = t[-2:]
			d = t[:10]
			
			utid = '%s_%s' % (uid, tid)
			ucid = '%s_%s' % (uid, cid)
			
			user_items.add('%s_%s' % (uid,tid))
			item_cat[tid] = cid
			
			
			i = i + 1
			if i%100000==0:
				#break
				print 'processed %d scores!' % i
			if d != day: # 只统计一天的数据
				continue
			
			AppendDict(user_active_hours, uid, h)
			AppendDict(item_active_hours, tid, h)
			AppendDict(cat_active_hours, cid, h)
			AppendDict(user_item_active_hours, utid, h)
			AppendDict(user_cat_active_hours, ucid, h)
			
			if row[2] == '1': # click
				IncDict(user_click_count, uid)
				IncDict(user_item_click_count, utid)
				IncDict(user_cat_click_count, ucid)
				
				IncDict(item_click_count, tid)
				
				IncDict(cat_click_count, cid)
				
				AppendDict(user_click_items, uid, tid)
				AppendDict(user_click_cats, uid, cid)
				
				
			elif row[2] == '2': # star
				IncDict(user_star_count, uid)
				IncDict(user_item_star_count, utid)
				IncDict(user_cat_star_count, ucid)
				
				IncDict(item_star_count, tid)
				
				IncDict(cat_star_count, cid)
				
				AppendDict(user_star_items, uid, tid)
				AppendDict(user_star_cats, uid, cid)
				
			elif row[2] == '3': # add to car
				IncDict(user_add_cart_count, uid)
				IncDict(user_item_add_cart_count, utid)
				IncDict(user_cat_add_cart_count, ucid)
				
				IncDict(item_add_cart_count, tid)
				
				IncDict(cat_add_cart_count, cid)
				
				AppendDict(user_add_cart_items, uid, tid)
				AppendDict(user_add_cart_cats, uid, cid)
				
			elif row[2] == '4':  # buy
				IncDict(user_buy_count, uid)
				IncDict(user_item_buy_count, utid)
				IncDict(user_cat_buy_count, ucid)
				
				IncDict(item_buy_count, tid)
				
				IncDict(cat_buy_count, cid)
				
				AppendDict(user_buy_items, uid, tid)
				AppendDict(user_buy_cats, uid, cid)
				
			
			
				
			
				
	# user feature
	#foutput = '%s_%s.csv' % ( util.file_basename(foutput), day )
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		
		"user_active_hours",
		"item_active_hours",
		"cat_active_hours",
		"user_item_active_hours",
		"user_cat_active_hours",
		"user_click_count",
		"user_star_count",
		"user_add_cart_count",
		"user_buy_count",
		"user_buy_items",
		"user_buy_cats",
		"user_click_items",
		"user_click_cats",
		"user_star_items",
		"user_star_cats",
		"user_add_cart_items",
		"user_add_cart_cats",
		"item_click_count",
		"item_star_count",
		"item_add_cart_count",
		"item_buy_count",
		"cat_click_count",
		"cat_star_count",
		"cat_add_cart_count",
		"cat_buy_count",
		"user_item_click_count",
		"user_item_star_count",
		"user_item_add_cart_count",
		"user_item_buy_count",
		"user_cat_click_count",
		"user_cat_star_count",
		"user_cat_add_cart_count",
		"user_cat_buy_count"
	])
	
	i = 0
	f = lambda x:DiffHours('%s 23' % lastday, x)+1
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			
			GetDict(user_active_hours, uid, len),
			GetDict(item_active_hours, tid, len),
			GetDict(cat_active_hours, cid, len),
			GetDict(user_item_active_hours, utid, len),
			GetDict(user_cat_active_hours, ucid, len),
			GetDict(user_click_count, uid),
			GetDict(user_star_count, uid),
			GetDict(user_add_cart_count, uid),
			GetDict(user_buy_count, uid),
			GetDict(user_buy_items, uid, len),
			GetDict(user_buy_cats, uid, len),
			GetDict(user_click_items, uid, len),
			GetDict(user_click_cats, uid, len),
			GetDict(user_star_items, uid, len),
			GetDict(user_star_cats, uid, len),
			GetDict(user_add_cart_items, uid, len),
			GetDict(user_add_cart_cats, uid, len),
			GetDict(item_click_count, tid),
			GetDict(item_star_count, tid),
			GetDict(item_add_cart_count, tid),
			GetDict(item_buy_count, tid),
			GetDict(cat_click_count, cid),
			GetDict(cat_star_count, cid),
			GetDict(cat_add_cart_count, cid),
			GetDict(cat_buy_count, cid),
			GetDict(user_item_click_count, utid),
			GetDict(user_item_star_count, utid),
			GetDict(user_item_add_cart_count, utid),
			GetDict(user_item_buy_count, utid),
			GetDict(user_cat_click_count, ucid),
			GetDict(user_cat_star_count, ucid),
			GetDict(user_cat_add_cart_count, ucid),
			GetDict(user_cat_buy_count, ucid),

			

			]
		
		fw.writerow(data)
		i = i + 1 
		if i%100000==0:
			print 'write %d rows.' % i 
			
	fd.close()	


if __name__ == '__main__':
	parser = OptionParser()

	parser.add_option('-m','--mode', dest='mode',help='mode, train, test')
	parser.add_option('-d','--day', default='2014-12-01', dest='day',help='day')
	parser.add_option('-f','--format',action="store_true", default=False, dest='f',help='format to copy')
	parser.add_option('-o','--out', dest='fn', default=r'featureTEST.csv', help='feature file to write')
	

	(options, args) = parser.parse_args()

	
	GenFeature('tianchi_mobile_recommend_train_user.csv', options.fn, day=options.day)
	