# coding:utf-8

import csv, time,sys, util, com
import numpy as np



# 特征生成文件9, item geo feature
item_geo = com.GetItemGeo()


geo_ids = set()
for v in item_geo.values():
	for g in v:
		geo_ids.add(g[:1])
		


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
			
			
			
			
			
				
			i = i + 1
			if i%100000==0:
				# break
				print 'processed %d scores!' % i
	
	
			
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id'] + ['item_geo_%s' % i for i in geo_ids])
	
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
			
			
		if int(tid) not in item_geo:
			geodata = [0 for g in geo_ids]
		else:
			geodata = []
			# print item_geo[int(tid)]
			for g in geo_ids:
				if g not in [ig[:1] for ig in item_geo[int(tid)]]:
					geodata.append(0)
				else:
					geodata.append(1)
	
		data = [uid, tid,
			] + geodata
		
		fw.writerow(data)
		
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__,sys.argv[1])