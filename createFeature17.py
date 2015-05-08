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
		return (d[key])
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
	user_item_last2day_add_car = dict()
	user_item_last2day_click = dict()
	user_item_last2day_star = dict()
	user_item_last2day_buy = dict()
	
	user_item_last3day_add_car = dict()
	user_item_last3day_click = dict()
	user_item_last3day_star = dict()
	user_item_last3day_buy = dict()
	
	user_item_1212_add_car = dict()
	user_item_1212_click = dict()
	user_item_1212_star = dict()
	user_item_1212_buy = dict()
	
	
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()

	with open(finput, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		header = reader.next()
		print header
		
		last2day = util.LastNDay(lastday,2)[:10]
		last3day = util.LastNDay(lastday,3)[:10]
		
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
			
			
			
			if t[:10]==last2day:
				if row[2]=='1': #click
					IncDict(user_item_last2day_click, utid)
				if row[2]=='2': #star 
					IncDict(user_item_last2day_star, utid)
				if row[2]=='3': # add car
					IncDict(user_item_last2day_add_car, utid)
				if row[2] == '4':  # buy
					IncDict(user_item_last2day_buy, utid)
			elif t[:10]==last3day:
				if row[2]=='1': #click
					IncDict(user_item_last3day_click, utid)
				if row[2]=='2': #star 
					IncDict(user_item_last3day_star, utid)
				if row[2]=='3': # add car
					IncDict(user_item_last3day_add_car, utid)
				if row[2] == '4':  # buy
					IncDict(user_item_last3day_buy, utid)
			elif t[:10]=='2014-12-12':
				if row[2]=='1': #click
					IncDict(user_item_1212_click, utid)
				if row[2]=='2': #star 
					IncDict(user_item_1212_star, utid)
				if row[2]=='3': # add car
					IncDict(user_item_1212_add_car, utid)
				if row[2] == '4':  # buy
					IncDict(user_item_1212_buy, utid)
			
				
				
				
			i = i + 1
			if i%100000==0:
				#break
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"user_item_last2day_click",
		"user_item_last2day_star",
		"user_item_last2day_add_car",
		"user_item_last2day_buy",
		"user_item_last3day_click",
		"user_item_last3day_star",
		"user_item_last3day_add_car",
		"user_item_last3day_buy",
		"user_item_1212_click",
		"user_item_1212_star",
		"user_item_1212_add_car",
		"user_item_1212_buy",
	])
	
	i = 0
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			GetDict(user_item_last2day_click, utid),
			GetDict(user_item_last2day_star, utid),
			GetDict(user_item_last2day_add_car, utid),
			GetDict(user_item_last2day_buy, utid),
			GetDict(user_item_last3day_click, utid),
			GetDict(user_item_last3day_star, utid),
			GetDict(user_item_last3day_add_car, utid),
			GetDict(user_item_last3day_buy, utid),
			GetDict(user_item_1212_click, utid),
			GetDict(user_item_1212_star, utid),
			GetDict(user_item_1212_add_car, utid),
			GetDict(user_item_1212_buy, utid),
			
			

			]
		
		fw.writerow(data)
		i = i + 1 
		if i%100000==0:
			print 'write %d rows.' % i 
			
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])