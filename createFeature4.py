# coding:utf-8

import csv, time,sys, util,com
import numpy as np



# 特征生成文件4
# user_item_click_nobuy = dict()

user_lastday_add_star = dict()
user_item_lastday_add_star = dict()
user_cat_lastday_add_star = dict()

user_lastday_add_cart = dict()
user_item_lastday_add_cart = dict()
user_cat_lastday_add_cart = dict()

user_lastday_buy = dict()
user_item_lastday_buy = dict()
user_cat_lastday_buy = dict()


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
	

	
	
	# 细化行为特征
	
	
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()

	with open(finput, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		header = reader.next()
		print header
		
		lastweek = util.LastWeek(lastday)
		halfmonth = util.HalfMonth(lastday)
		
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
			
			#diff_time = DiffTime('%s 00' % lastday, row[5]) + 24*3600
			
			
			if row[5][:10]==lastday:  # lastday
				
				
				if row[2] == '1': # click
					pass
						
				if row[2] == '2': # star
					IncDict(user_lastday_add_star, uid)
					IncDict(user_item_lastday_add_star, utid)
					IncDict(user_cat_lastday_add_star, ucid)
						
				if row[2] == '3': # add to car
					IncDict(user_lastday_add_cart, uid)
					IncDict(user_item_lastday_add_cart, utid)
					IncDict(user_cat_lastday_add_cart, ucid)
					
						
				if row[2] == '4':  # buy
					IncDict(user_lastday_buy, uid)
					IncDict(user_item_lastday_buy, utid)
					IncDict(user_cat_lastday_buy, ucid)
					
				
				
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"user_lastday_add_star",
		"user_item_lastday_add_star",
		"user_cat_lastday_add_star",
		"user_lastday_add_cart",
		"user_item_lastday_add_cart",
		"user_cat_lastday_add_cart",
		"user_lastday_buy",
		"user_item_lastday_buy",
		"user_cat_lastday_buy"
	])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDict(user_lastday_add_star, uid),
			GetDict(user_item_lastday_add_star, utid),
			GetDict(user_cat_lastday_add_star, ucid),
			GetDict(user_lastday_add_cart, uid),
			GetDict(user_item_lastday_add_cart, utid),
			GetDict(user_cat_lastday_add_cart, ucid),
			GetDict(user_lastday_buy, uid),
			GetDict(user_item_lastday_buy, utid),
			GetDict(user_cat_lastday_buy, ucid),
			]
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])