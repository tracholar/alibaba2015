# coding:utf-8
'''
生成用户地理位置的最精确特征
用户是不是在非常热门那几个小区域
'''

import csv, time,sys, util,com
import numpy as np



# 特征生成文件1, user geo feature


T = com.GetGeoTree()

geo_tree = {}

user_in_geotrees_list = []

rules = [(1, 1e5), (2,1e5),(3,1e5),(4,1e4),(5,5e3),(6,1e3), (7,1e2)]
for r in rules:
	geo_tree.update({i:T[i] for i in T if T[i]>r[1] and len(i)==r[0]})
	user_in_geotrees_list.append(dict())    # 用户的geohash是否在上述geo_tree中



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
			
			# diff_time = DiffTime('%s 00' % lastday, row[5]) + 24*24*3600
			
			
			
			
			geoid = row[3]
			
			for j in range(len(user_in_geotrees_list)):
				user_in_geotrees = user_in_geotrees_list[j]
				if uid not in user_in_geotrees:
					user_in_geotrees[uid] = 0	
				
				if geoid is not '':
					
					if geoid[:rules[j][0]] in geo_tree:
						user_in_geotrees[uid] = 1
					
			
				
			i = i + 1
			if i%100000==0:
				#break
				print 'processed %d scores!' % i
	
	
			
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')
	header = ['user_id', 'item_id',]
	for i in range(len(user_in_geotrees_list)):
		header.append( 'user_in_hot_pos_%d' % (1+i))
	fw.writerow(header)
	i = 0
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
			
		geodata = []	
		for j in range(len(user_in_geotrees_list)):
			geodata.append( GetDict(user_in_geotrees_list[j], uid))
			
	
		data = [uid, tid,] + geodata
		
		fw.writerow(data)
		
		i = i + 1
		if i%100000==0:
			print 'write %d rows!' % i
	
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])