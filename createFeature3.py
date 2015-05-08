# coding:utf-8

import csv, time,sys, util,com
import numpy as np



# 特征生成文件2

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
	user_cat_lastweek_click = dict()
	user_cat_lastweek_star = dict()
	user_cat_lastweek_add_car = dict()
	user_cat_lastweek_buy = dict()
	
	user_cat_halfmonth_click = dict()
	user_cat_halfmonth_star = dict()
	user_cat_halfmonth_add_car = dict()
	user_cat_halfmonth_buy = dict()
	
	user_cat_before_halfmonth_click = dict()
	user_cat_before_halfmonth_star = dict()
	user_cat_before_halfmonth_add_car = dict()
	user_cat_before_halfmonth_buy = dict()
	
	
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
			
			
			
			
			if row[5][:10]==lastday:  # lastday
				
				continue
				
			
			if row[2] == '1': # click
				if t>lastweek: # lastweek
					
					IncDict(user_cat_lastweek_click, ucid)
				elif t > halfmonth: # last half month
					IncDict(user_cat_halfmonth_click, ucid)
				else:  # before half month
					IncDict(user_cat_before_halfmonth_click, ucid)
			if row[2] == '2': # star
				
	
				if t > lastweek: # lastweek
					IncDict(user_cat_lastweek_star, ucid)
				elif t > halfmonth: # last half month
					IncDict(user_cat_halfmonth_star, ucid)
				else:  # before half month
					IncDict(user_cat_before_halfmonth_star, ucid)
					
			if row[2] == '3': # add to car
				
				
				if t > lastweek: # lastweek
					IncDict(user_cat_lastweek_add_car, ucid)
				elif t > halfmonth: # last half month
					IncDict(user_cat_halfmonth_add_car, ucid)
				else:  # before half month
					IncDict(user_cat_before_halfmonth_add_car, ucid)
					
					
			if row[2] == '4':  # buy
				
				
				# print utid
				if t > lastweek: # lastweek
					IncDict(user_cat_lastweek_buy, ucid)
			
				elif t > halfmonth: # last half month
					IncDict(user_cat_halfmonth_buy, ucid)
				else:  # before half month
					IncDict(user_cat_before_halfmonth_buy, ucid)
			
			
				
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"user_cat_lastweek_click",
		"user_cat_lastweek_star",
		"user_cat_lastweek_add_car",
		"user_cat_lastweek_buy",
		"user_cat_halfmonth_click",
		"user_cat_halfmonth_star",
		"user_cat_halfmonth_add_car",
		"user_cat_halfmonth_buy",
		"user_cat_before_halfmonth_click",
		"user_cat_before_halfmonth_star",
		"user_cat_before_halfmonth_add_car",
		"user_cat_before_halfmonth_buy"
	])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDict(user_cat_lastweek_click, ucid),
			GetDict(user_cat_lastweek_star, ucid),
			GetDict(user_cat_lastweek_add_car, ucid),
			GetDict(user_cat_lastweek_buy, ucid),
			GetDict(user_cat_halfmonth_click, ucid),
			GetDict(user_cat_halfmonth_star, ucid),
			GetDict(user_cat_halfmonth_add_car, ucid),
			GetDict(user_cat_halfmonth_buy, ucid),
			GetDict(user_cat_before_halfmonth_click, ucid),
			GetDict(user_cat_before_halfmonth_star, ucid),
			GetDict(user_cat_before_halfmonth_add_car, ucid),
			GetDict(user_cat_before_halfmonth_buy, ucid),

			]
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])