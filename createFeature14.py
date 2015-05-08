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
	item_lastday_click = dict()
	item_lastday_star = dict()
	item_lastday_add_car = dict()
	item_lastday_buy = dict()
	
	
	item_lastweek_click = dict()
	item_lastweek_star = dict()
	item_lastweek_add_car = dict()
	item_lastweek_buy = dict()
	
	item_halfmonth_click = dict()
	item_halfmonth_star = dict()
	item_halfmonth_add_car = dict()
	item_halfmonth_buy = dict()
	
	item_before_halfmonth_click = dict()
	item_before_halfmonth_star = dict()
	item_before_halfmonth_add_car = dict()
	item_before_halfmonth_buy = dict()
	
	
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
			
			
			
				
			
			if row[2] == '1': # click
				if row[5][:10]==lastday:  # lastday
					IncDict(item_lastday_click, tid)
				
				elif t > lastweek: # lastweek
					
					IncDict(item_lastweek_click, tid)
				elif t > halfmonth: # last half month
					IncDict(item_halfmonth_click, tid)
				else:  # before half month
					IncDict(item_before_halfmonth_click, tid)
			if row[2] == '2': # star
				if row[5][:10]==lastday:  # lastday
					IncDict(item_lastday_star, tid)
				
				elif t > lastweek: # lastweek
					IncDict(item_lastweek_star, tid)
				elif t > halfmonth: # last half month
					IncDict(item_halfmonth_star, tid)
				else:  # before half month
					IncDict(item_before_halfmonth_star, tid)
					
			if row[2] == '3': # add to car
				
				if row[5][:10]==lastday:  # lastday
					IncDict(item_lastday_add_car, tid)
				
				elif t > lastweek: # lastweek
					IncDict(item_lastweek_add_car, tid)
				elif t > halfmonth: # last half month
					IncDict(item_halfmonth_add_car, tid)
				else:  # before half month
					IncDict(item_before_halfmonth_add_car, tid)
					
					
			if row[2] == '4':  # buy
				
				
				# print utid
				if row[5][:10]==lastday:  # lastday
					IncDict(item_lastday_buy, tid)
				
				elif t > lastweek: # lastweek
					IncDict(item_lastweek_buy, tid)
			
				elif t > halfmonth: # last half month
					IncDict(item_halfmonth_buy, tid)
				else:  # before half month
					IncDict(item_before_halfmonth_buy, tid)
			
			
				
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"item_lastday_click",
		"item_lastday_star",
		"item_lastday_add_car",
		"item_lastday_buy",
		
		"item_lastweek_click",
		"item_lastweek_star",
		"item_lastweek_add_car",
		"item_lastweek_buy",
		"item_halfmonth_click",
		"item_halfmonth_star",
		"item_halfmonth_add_car",
		"item_halfmonth_buy",
		"item_before_halfmonth_click",
		"item_before_halfmonth_star",
		"item_before_halfmonth_add_car",
		"item_before_halfmonth_buy"
	])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDict(item_lastday_click, tid),
			GetDict(item_lastday_star, tid),
			GetDict(item_lastday_add_car, tid),
			GetDict(item_lastday_buy, tid),
			
			GetDict(item_lastweek_click, tid),
			GetDict(item_lastweek_star, tid),
			GetDict(item_lastweek_add_car, tid),
			GetDict(item_lastweek_buy, tid),
			GetDict(item_halfmonth_click, tid),
			GetDict(item_halfmonth_star, tid),
			GetDict(item_halfmonth_add_car, tid),
			GetDict(item_halfmonth_buy, tid),
			GetDict(item_before_halfmonth_click, tid),
			GetDict(item_before_halfmonth_star, tid),
			GetDict(item_before_halfmonth_add_car, tid),
			GetDict(item_before_halfmonth_buy, tid),

			]
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])