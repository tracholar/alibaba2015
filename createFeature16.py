# coding:utf-8

import csv, time,sys, util,com
import numpy as np



# 特征生成文件2

def IncDict(d, key):
	if key in d:
		d[key] = d[key] + 1
	else:
		d[key] = 1

def GetDictCount(d, key):
	if key in d:
		return len(d[key])
	else:
		return 0
def DiffTime(t1, t2):
	t1 = time.mktime(time.strptime(t1,'%Y-%m-%d %H'))
	t2 = time.mktime(time.strptime(t2,'%Y-%m-%d %H'))
	return t1 - t2
	
	
def GenFeature(finput='user_action_train.csv', foutput = 'feature.csv', lastday = '2014-12-18'):
	

	
	
	# 细化行为特征
	# 用户买的物品数目
	#
	user_buy_item_number = dict()
	user_buy_cat_number = dict()
	
	
	
	
	item_buy_user_number = dict()
	cat_buy_user_number = dict()
	
	user_click_items = dict()
	user_buy_items = dict()
	user_buy_cats = dict()
	
	item_buy_users = dict()
	cat_buy_users = dict()
	
	
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
			
			#diff_time = DiffTime('%s 00' % lastday, row[5]) + 24*3600
			
			
			
			if row[2]=='1': #click
				if uid not in user_click_items:
					user_click_items[uid] = set()
				user_click_items[uid].add(tid)
				
			if row[2] == '4':  # buy
				if uid not in user_buy_items:
					user_buy_items[uid] = set()
				if uid not in user_buy_cats:
					user_buy_cats[uid] = set()
				if tid not in item_buy_users:
					item_buy_users[tid] = set()
				if cid not in cat_buy_users:
					cat_buy_users[cid] = set()
				user_buy_items[uid].add(tid)
				user_buy_cats[uid].add(cid)
				item_buy_users[tid].add(uid)
				cat_buy_users[cid].add(uid)
				
				
				
			i = i + 1
			if i%100000==0:
				#break
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"user_buy_item_number",
		"user_buy_cat_number",
		"item_buy_user_number",
		"cat_buy_user_number",
		"user_click_item_number",
	])
	
	i = 0
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDictCount(user_buy_items, uid),
			GetDictCount(user_buy_cats, uid),
			GetDictCount(item_buy_users, tid),
			GetDictCount(cat_buy_users, cid),
			GetDictCount(user_click_items, uid),

			]
		
		fw.writerow(data)
		i = i + 1 
		if i%100000==0:
			print 'write %d rows.' % i 
			
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])