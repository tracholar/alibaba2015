# coding:utf-8

import csv, time,sys,util,com
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
	user_item_lastThreeDay_click = dict()
	user_item_lastThreeDay_star = dict()
	user_item_lastThreeDay_add_car = dict()
	user_item_lastThreeDay_buy = dict()
	
	user_item_lastSixDay_click = dict()
	user_item_lastSixDay_star = dict()
	user_item_lastSixDay_add_car = dict()
	user_item_lastSixDay_buy = dict()
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()

	with open(finput, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		header = reader.next()
		print header
		
		last3day = util.LastNDay(lastday, 3)
		last6day = util.LastNDay(lastday, 6)
		
		
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
			
			# diff_time = DiffTime('%s 00' % lastday, row[5])
			
			
			
			if row[2] == '1': # click
				if t > last3day: # last three day
					
					IncDict(user_item_lastThreeDay_click, utid)
				elif t > last6day: # last six day
					IncDict(user_item_lastSixDay_click, utid)
				else:  # before six month
					pass
			if row[2] == '2': # star
				
	
				if t > last3day: # last three day
					IncDict(user_item_lastThreeDay_star, utid)
				elif t > last6day: # last six day
					IncDict(user_item_lastSixDay_star, utid)
				else:  # before half month
					pass
					
			if row[2] == '3': # add to car
				
				
				if t > last3day: # last three day
					IncDict(user_item_lastThreeDay_add_car, utid)
				elif t > last6day: # last six day
					IncDict(user_item_lastSixDay_add_car, utid)
				else:  # before half month
					pass
					
					
			if row[2] == '4':  # buy
				
				
				# print utid
				if t > last3day: # last three day
					IncDict(user_item_lastThreeDay_buy, utid)
			
				elif t > last6day: # last six day
					IncDict(user_item_lastSixDay_buy, utid)
				else:  # before half month
					pass
			
			
				
			i = i + 1
			if i%100000==0:
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"user_item_aveThreeDayDelta_click",
		"user_item_aveThreeDayDelta_star",
		"user_item_aveThreeDayDelta_add_car",
		"user_item_aveThreeDayDelta_buy",
	])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDict(user_item_lastSixDay_click, utid)-GetDict(user_item_lastThreeDay_click, utid),
			GetDict(user_item_lastSixDay_star, utid)-GetDict(user_item_lastThreeDay_star, utid),
			GetDict(user_item_lastSixDay_add_car, utid)-GetDict(user_item_lastThreeDay_add_car, utid),
			GetDict(user_item_lastSixDay_buy, utid)-GetDict(user_item_lastThreeDay_buy, utid),
			]
		
		fw.writerow(data)
		
	fd.close()	


	
if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])