# coding:utf-8

import csv, time,sys, util,com
import numpy as np



# 特征生成文件13

user_item_lastday_click_nobuy = dict()
user_item_lastday_star_nobuy = dict()
user_item_lastday_cart_nobuy = dict()
user_item_lastday_buy_again = dict()

user_item_click = set()
user_item_star = set()
user_item_cart = set()
user_item_buy = set()


user_cat_lastday_click_nobuy = dict()
user_cat_lastday_star_nobuy = dict()
user_cat_lastday_cart_nobuy = dict()
user_cat_lastday_buy_again = dict()

user_cat_click = set()
user_cat_star = set()
user_cat_cart = set()
user_cat_buy = set()


cat_lastday_click_nobuy = dict()
cat_lastday_star_nobuy = dict()
cat_lastday_cart_nobuy = dict()
cat_lastday_buy_again = dict()

cat_click = set()
cat_star = set()
cat_cart = set()
cat_buy = set()


item_lastday_click_nobuy = dict()
item_lastday_star_nobuy = dict()
item_lastday_cart_nobuy = dict()
item_lastday_buy_again = dict()

item_click = set()
item_star = set()
item_cart = set()
item_buy = set()


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
def parse_time(t):
	return time.mktime(time.strptime(t,'%Y-%m-%d %H'))

def AddLastTime(time_dict, utid, t):
	if utid not in time_dict:
		time_dict[utid] = t
		return
	
	if DiffTime(time_dict[utid], t)<0:
		time_dict[utid] = t
		return
	
		
	
def JugeDoingNobuy(d,last_doing_set, last_doing_time, utid):
	if utid not in last_doing_set: # no doing
		d[utid] = 0
		return
	
	if utid not in user_item_buy: # not buy
		d[utid] = 1
		return
	
	
	do_t = last_doing_time[utid]
	buy_t = user_item_last_buy_time[utid]
	
	diff_time = DiffTime(do_t, buy_t)
	if diff_time > 0:
		d[utid] = 0 
		return
		
	d[utid] = 1
	# print utid
	
	
def GenFeature(finput='user_action_train.csv', foutput = 'feature.csv', lastday = '2014-12-18'):
	

	
	
	# 细化行为特征
	
	
	
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
			t = row[5]
			
			utid = '%s_%s' % (uid, tid)
			ucid = '%s_%s' % (uid, cid)
			
			user_items.add('%s_%s' % (uid,tid))
			item_cat[tid] = cid
			
			# diff_time = DiffTime('%s 00' % lastday, row[5]) + 24*3600
			#if diff_time >=0 : # 未来的数据
			#	continue
			
			
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
				
			if t[:len(lastday)]!=lastday:  # 只统计最后一天
				continue
				
				
			if row[2] == '1': # click
				user_item_click.add(utid)
				user_cat_click.add(ucid)
				cat_click.add(cid)
				item_click.add(tid)
					
			if row[2] == '2': # star
				user_item_star.add(utid)
				user_cat_star.add(ucid)
				cat_star.add(cid)
				item_star.add(tid)
				
			if row[2] == '3': # add to car
				user_item_cart.add(utid)
				user_cat_cart.add(ucid)
				cat_cart.add(cid)
				item_cart.add(tid)
				
			if row[2] == '4':  # buy
				
				if ucid in user_cat_buy:
					user_item_lastday_buy_again[utid] = 1
					user_cat_lastday_buy_again[ucid] = 1
					cat_lastday_buy_again[cid] = 1
					item_lastday_buy_again[tid] = 1
				else:
					user_item_buy.add(utid)
					user_cat_buy.add(ucid)
					cat_buy.add(cid)
					item_buy.add(tid)
			
				
			
	user_item_lastday_click_nobuy = {id:1 for id in (user_item_click - user_item_buy)}
	user_item_lastday_star_nobuy = {id:1 for id in (user_item_star - user_item_buy)}
	user_item_lastday_cart_nobuy = {id:1 for id in (user_item_cart - user_item_buy)}
	
	
	user_cat_lastday_click_nobuy = {id:1 for id in (user_cat_click - user_cat_buy)}
	user_cat_lastday_star_nobuy = {id:1 for id in (user_cat_star - user_cat_buy)}
	user_cat_lastday_cart_nobuy = {id:1 for id in (user_cat_cart - user_cat_buy)}
	
	cat_lastday_click_nobuy = {id:1 for id in (cat_click - cat_buy)}
	cat_lastday_star_nobuy = {id:1 for id in (cat_star - cat_buy)}
	cat_lastday_cart_nobuy = {id:1 for id in (cat_cart - cat_buy)}
	
	item_lastday_click_nobuy = {id:1 for id in (item_click - item_buy)}
	item_lastday_star_nobuy = {id:1 for id in (item_star - item_buy)}
	item_lastday_cart_nobuy = {id:1 for id in (item_cart - item_buy)}
	
	
	# write feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"user_item_lastday_click_nobuy",
		"user_item_lastday_star_nobuy",
		"user_item_lastday_cart_nobuy",
		"user_item_lastday_buy_again",


		"user_cat_lastday_click_nobuy",
		"user_cat_lastday_star_nobuy",
		"user_cat_lastday_cart_nobuy",
		"user_cat_lastday_buy_again",
		
		"cat_lastday_click_nobuy",
		"cat_lastday_star_nobuy",
		"cat_lastday_cart_nobuy",
		"cat_lastday_buy_again",
		
		"item_lastday_click_nobuy",
		"item_lastday_star_nobuy",
		"item_lastday_cart_nobuy",
		"item_lastday_buy_again"
	])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
			
			
		
		
	
		data = [uid, tid,
			GetDict(user_item_lastday_click_nobuy, utid),
			GetDict(user_item_lastday_star_nobuy, utid),
			GetDict(user_item_lastday_cart_nobuy, utid),
			GetDict(user_item_lastday_buy_again, utid),


			GetDict(user_cat_lastday_click_nobuy, ucid),
			GetDict(user_cat_lastday_star_nobuy, ucid),
			GetDict(user_cat_lastday_cart_nobuy, ucid),
			GetDict(user_cat_lastday_buy_again, ucid),
			
			GetDict(cat_lastday_click_nobuy, cid),
			GetDict(cat_lastday_star_nobuy, cid),
			GetDict(cat_lastday_cart_nobuy, cid),
			GetDict(cat_lastday_buy_again, cid),
			
			GetDict(item_lastday_click_nobuy, tid),
			GetDict(item_lastday_star_nobuy, tid),
			GetDict(item_lastday_cart_nobuy, tid),
			GetDict(item_lastday_buy_again, tid),
			]
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])