# coding:utf-8

import csv, time,sys, com
import numpy as np
from com import GetRecItems


# 用户总活跃度(所有行为次数之和)
# 最后一天活跃度(最后一天活跃次数)
# 用户转化率(购买次数/总行为次数)，
# 物品流行度(物品被行为的总和)
# 物品最后一天活跃度
# 物品转化率(被购买次数/总行为次数)
# 物品分类的流行度
# 物品分类的转化率
# 用户对该品牌的活跃度
# 用户对该品牌最后一天的活跃度
# 用户对该物品的活跃度
# 用户对该物品最后一天的活跃度

def IncDict(d, key):
	if key in d:
		d[key] = d[key] + 1
	else:
		d[key] = 1

def GetDict(d, key):
	if key in d:
		return d[key]
	else:
		return 0
def DiffTime(t1, t2):
	t1 = time.mktime(time.strptime(t1,'%Y-%m-%d %H'))
	t2 = time.mktime(time.strptime(t2,'%Y-%m-%d %H'))
	return t1 - t2
	
	
def GenFeature(finput='user_action_train.csv', foutput = 'feature.csv', lastday = '2014-12-18'):
	user_action_count = dict()
	user_lastday_count = dict()
	user_buy_count = dict()
	item_click_count = dict()
	item_lastday_count = dict()
	item_buy_count = dict()
	cat_click_count = dict()
	cat_buy_count = dict()
	user_cat_count = dict()
	user_cat_lastday_count = dict()
	user_item_count = dict()
	user_item_lastday_count = dict()

	user_add_car = dict()
	user_add_star = dict()
	item_added_car = dict()
	item_added_start = dict()
	user_item_lasttime = dict()
	
	cat_add_car = dict()
	cat_add_star = dict()
	
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()

	with open(finput, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		header = reader.next()
		print header
		
		i = 0
		for row in reader:
			if row[5] > '%s 23' % lastday : # 未来的数据
				continue
			
			uid = row[0]
			tid = row[1]
			cid = row[4]
			
			utid = '%s_%s' % (uid, tid)
			ucid = '%s_%s' % (uid, cid)
			
			user_items.add('%s_%s' % (uid,tid))
			item_cat[tid] = cid
			
			
			
			#print diff_time, diff_time<6*24*3600
			
			IncDict(user_action_count, uid)
			IncDict(item_click_count, tid)
			IncDict(cat_click_count, cid)
			IncDict(user_cat_count, '%s_%s' % (uid,cid))
			IncDict(user_item_count, '%s_%s' % (uid,tid))
			
			if row[5][:10]==lastday:  # lastday
				IncDict(user_lastday_count, uid)
				IncDict(item_lastday_count, tid)
				IncDict(user_cat_lastday_count, '%s_%s' % (uid,cid))
				IncDict(user_item_lastday_count, '%s_%s' % (uid,tid))
			
			
			#if row[2] == '1': # click
			#	if diff_time < 6*24*3600: # lastweek
			#		IncDict(user_item_lastweek_click, utid)
					
			if row[2] == '2': # star
				IncDict(user_add_star, uid)
				IncDict(item_added_start, tid)
				
				IncDict(cat_add_star, cid)
	
				#if diff_time < 6*24*3600: # lastweek
				#	IncDict(user_item_lastweek_star, utid)
				
			if row[2] == '3': # add to car
				IncDict(user_add_car, uid)
				IncDict(item_added_car, tid)
				
				IncDict(cat_add_car, cid)
				
				#if diff_time < 6*24*3600: # lastweek
				#	IncDict(user_item_lastweek_add_car, utid)
	
			if row[2] == '4':  # buy
				IncDict(user_buy_count, uid)
				IncDict(item_buy_count, tid)
				IncDict(cat_buy_count, cid)
				
				
				
				#if diff_time < 6*24*3600: # lastweek
				#	IncDict(user_item_lastweek_buy, utid)
			
			key = '%s_%s' % (uid,tid)
			if key in user_item_lasttime:
				diff_time = DiffTime(user_item_lasttime[key], row[5])
				if diff_time<0:
					user_item_lasttime[key] = row[5]
			else:
				user_item_lasttime[key] = row[5]
			
				
				
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',"user_action_count", 
		"user_lastday_count", "user_buy_count", "item_click_count",
		"item_lastday_count", "item_buy_count", "cat_click_count", 
		"cat_buy_count", "user_cat_count", "user_cat_lastday_count", 
		"user_item_count", "user_item_lastday_count",
		"user_add_car", "user_add_star","item_added_car","item_added_start",
		"user_item_lasttime",
		"cat_add_car", "cat_add_star"
		])
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		
		data = [uid, tid,
			GetDict(user_action_count, uid),
			GetDict(user_lastday_count, uid),
			GetDict(user_buy_count, uid),
			GetDict(item_click_count, tid),
			GetDict(item_lastday_count, tid),
			GetDict(item_buy_count, tid),
			GetDict(cat_click_count, cid),
			GetDict(cat_buy_count, cid),
			GetDict(user_cat_count, '%s_%s' % (uid, cid)),
			GetDict(user_cat_lastday_count, '%s_%s' % (uid, cid)),
			GetDict(user_item_count, '%s_%s' % (uid, tid)),
			GetDict(user_item_lastday_count, '%s_%s' % (uid, tid)),
			GetDict(user_add_car, uid),
			GetDict(user_add_star, uid),
			GetDict(item_added_car, tid),
			GetDict(item_added_start, tid),
			
			DiffTime('%s 00' % lastday, row[5]) + 24*24*3600,
			GetDict(cat_add_car, cid),
			GetDict(cat_add_star, cid)
			
			
			
			]
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])