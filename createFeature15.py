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
	cat_lastday_click = dict()
	cat_lastday_star = dict()
	cat_lastday_add_car = dict()
	cat_lastday_buy = dict()
	
	
	cat_lastweek_click = dict()
	cat_lastweek_star = dict()
	cat_lastweek_add_car = dict()
	cat_lastweek_buy = dict()
	
	cat_halfmonth_click = dict()
	cat_halfmonth_star = dict()
	cat_halfmonth_add_car = dict()
	cat_halfmonth_buy = dict()
	
	cat_before_halfmonth_click = dict()
	cat_before_halfmonth_star = dict()
	cat_before_halfmonth_add_car = dict()
	cat_before_halfmonth_buy = dict()
	
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()
	
	lastweek = util.LastWeek(lastday)
	halfmonth = util.HalfMonth(lastday)
		
		

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
			
			
				
			
			if row[2] == '1': # click
				if row[5][:10]==lastday:  # lastday
					IncDict(cat_lastday_click, cid)
				
				elif t > lastweek: # lastweek
					
					IncDict(cat_lastweek_click, cid)
				elif t > halfmonth: # last half month
					IncDict(cat_halfmonth_click, cid)
				else:  # before half month
					IncDict(cat_before_halfmonth_click, cid)
			if row[2] == '2': # star
				if row[5][:10]==lastday:  # lastday
					IncDict(cat_lastday_star, cid)
				
				elif t > lastweek: # lastweek
					IncDict(cat_lastweek_star, cid)
				elif t > halfmonth: # last half month
					IncDict(cat_halfmonth_star, cid)
				else:  # before half month
					IncDict(cat_before_halfmonth_star, cid)
					
			if row[2] == '3': # add to car
				
				if row[5][:10]==lastday:  # lastday
					IncDict(cat_lastday_add_car, cid)
				
				elif t > lastweek: # lastweek
					IncDict(cat_lastweek_add_car, cid)
				elif t > halfmonth: # last half month
					IncDict(cat_halfmonth_add_car, cid)
				else:  # before half month
					IncDict(cat_before_halfmonth_add_car, cid)
					
					
			if row[2] == '4':  # buy
				
				
				# print ucid
				if row[5][:10]==lastday:  # lastday
					IncDict(cat_lastday_buy, cid)
				
				elif t > lastweek: # lastweek
					IncDict(cat_lastweek_buy, cid)
			
				elif t > halfmonth: # last half month
					IncDict(cat_halfmonth_buy, cid)
				else:  # before half month
					IncDict(cat_before_halfmonth_buy, cid)
			
			
				
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"cat_lastday_click",
		"cat_lastday_star",
		"cat_lastday_add_car",
		"cat_lastday_buy",
		
		"cat_lastweek_click",
		"cat_lastweek_star",
		"cat_lastweek_add_car",
		"cat_lastweek_buy",
		"cat_halfmonth_click",
		"cat_halfmonth_star",
		"cat_halfmonth_add_car",
		"cat_halfmonth_buy",
		"cat_before_halfmonth_click",
		"cat_before_halfmonth_star",
		"cat_before_halfmonth_add_car",
		"cat_before_halfmonth_buy"
	])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDict(cat_lastday_click, cid),
			GetDict(cat_lastday_star, cid),
			GetDict(cat_lastday_add_car, cid),
			GetDict(cat_lastday_buy, cid),
			
			GetDict(cat_lastweek_click, cid),
			GetDict(cat_lastweek_star, cid),
			GetDict(cat_lastweek_add_car, cid),
			GetDict(cat_lastweek_buy, cid),
			GetDict(cat_halfmonth_click, cid),
			GetDict(cat_halfmonth_star, cid),
			GetDict(cat_halfmonth_add_car, cid),
			GetDict(cat_halfmonth_buy, cid),
			GetDict(cat_before_halfmonth_click, cid),
			GetDict(cat_before_halfmonth_star, cid),
			GetDict(cat_before_halfmonth_add_car, cid),
			GetDict(cat_before_halfmonth_buy, cid),

			]
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])