# coding:utf-8

import csv, time,sys, util,com
import numpy as np



# 特征生成文件2

def IncDict(d, key):
	if key in d:
		d[key] = d[key] + 1
	else:
		d[key] = 1
def AppendDict(d,key,val):
	if key not in d:
		d[key] = set()
	
	d[key].add(val)
	
def GetDict(d, key, f=lambda x:x):
	if key in d:
		return f(d[key])
	else:
		return 0

def DiffTime(t1, t2):
	t1 = time.mktime(time.strptime(t1,'%Y-%m-%d %H'))
	t2 = time.mktime(time.strptime(t2,'%Y-%m-%d %H'))
	return t1 - t2
def GetHours(t): # 距离7月1日0点的小时数
	m = int(t[5:7])
	d = int(t[8:10])
	h = int(t[11:])
	return ((m-7)*31+d-1)*24+h 
def DiffHours(t1, t2):
	return GetHours(t1) - GetHours(t2)
	
	
def GenFeature(finput='user_action_train.csv', foutput = 'feature.csv', lastday = '2014-12-18'):
	

	
	
	# 细化行为特征
	# 用户买的物品数目
	#
	
	user_active_days = dict()
	item_active_days = dict()
	cat_active_days = dict()
	
	user_lastweek_active_days = dict()
	item_lastweek_active_days = dict()
	cat_lastweek_active_days = dict()
	
	user_item_active_days = dict()
	user_item_lastweek_active_days = dict()
	user_cat_active_days = dict()
	user_cat_lastweek_active_days = dict()
	
	
	
	user_lastday_active_hours = dict()
	item_lastday_active_hours = dict()
	user_item_lastday_active_hours = dict()
	cat_lastday_active_hours = dict()
	user_cat_lastday_active_hours = dict()
	
	user_last_active_time = dict()
	item_last_active_time = dict()
	cat_last_active_time = dict()
	user_item_last_active_time = dict()
	user_cat_last_active_time = dict()
	
	
	
	user_items = set()  # 其实是用户物品对
	item_cat = dict()

	with open(finput, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		header = reader.next()
		print header
		
		last7day = util.LastNDay(lastday,7)[:10]
		
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
			
			
			AppendDict(user_active_days, uid, t[:10])
			AppendDict(item_active_days, tid, t[:10])
			AppendDict(user_item_active_days, utid, t[:10])
			AppendDict(cat_active_days, cid, t[:10])
			AppendDict(user_cat_active_days, ucid, t[:10])
			
			if t[:10]==lastday: #last day
				AppendDict(user_lastday_active_hours, uid, t[11:])
				AppendDict(item_lastday_active_hours, tid, t[11:])
				AppendDict(user_item_lastday_active_hours, utid, t[11:])
				AppendDict(cat_lastday_active_hours, cid, t[11:])
				AppendDict(user_cat_lastday_active_hours, ucid, t[11:])
				
			if t[:10]>=last7day: # last week
				AppendDict(user_lastweek_active_days, uid, t[:10])
				AppendDict(item_lastweek_active_days, tid, t[:10])
				AppendDict(user_item_lastweek_active_days, utid, t[:10])
				AppendDict(cat_lastweek_active_days, cid, t[:10])
				AppendDict(user_cat_active_days, ucid, t[:10])
				
			if uid not in user_last_active_time or user_last_active_time[uid]<t:
				user_last_active_time[uid] = t
			if tid not in item_last_active_time or item_last_active_time[tid]<t:
				item_last_active_time[tid] = t
			if cid not in cat_last_active_time or cat_last_active_time[cid] < t:
				cat_last_active_time[cid] = t
			if utid not in user_item_last_active_time or user_item_last_active_time[ucid] < t:
				user_item_last_active_time[ucid] = t
			if ucid not in user_cat_last_active_time or user_cat_last_active_time[ucid] < t:
				user_cat_last_active_time[ucid] = t
			
				
			i = i + 1
			if i%100000==0:
				#break
				print 'processed %d scores!' % i
				
	# user feature
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		
		"user_active_days",
		"item_active_days",
		"cat_active_days",
		"user_lastweek_active_days",
		"item_lastweek_active_days",
		"cat_lastweek_active_days",
		"user_item_active_days",
		"user_item_lastweek_active_days",
		"user_cat_active_days",
		"user_cat_lastweek_active_days",
		"user_lastday_active_hours",
		"item_lastday_active_hours",
		"user_item_lastday_active_hours",
		"cat_lastday_active_hours",
		"user_cat_lastday_active_hours",
		"user_last_active_time",
		"item_last_active_time",
		"cat_last_active_time",
		"user_item_last_active_time",
		"user_cat_last_active_time"
	])
	
	i = 0
	f = lambda x:DiffHours('%s 23' % lastday, x)+1
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
		
		data = [uid, tid,
			
			GetDict(user_active_days, uid, len),
			GetDict(item_active_days, tid, len),
			GetDict(cat_active_days, cid, len),
			GetDict(user_lastweek_active_days, uid, len),
			GetDict(item_lastweek_active_days, tid, len),
			GetDict(cat_lastweek_active_days, cid, len),
			GetDict(user_item_active_days, utid, len),
			GetDict(user_item_lastweek_active_days, utid, len),
			GetDict(user_cat_active_days, ucid, len),
			GetDict(user_cat_lastweek_active_days, ucid, len),
			GetDict(user_lastday_active_hours, uid, len),
			GetDict(item_lastday_active_hours, tid, len),
			GetDict(user_item_lastday_active_hours, utid, len),
			GetDict(cat_lastday_active_hours, cid, len),
			GetDict(user_cat_lastday_active_hours, ucid, len),
			GetDict(user_last_active_time, uid, f),
			GetDict(item_last_active_time, tid, f),
			GetDict(cat_last_active_time, cid, f),
			GetDict(user_item_last_active_time, utid, f),
			GetDict(user_cat_last_active_time, ucid, f),
			
			

			]
		
		fw.writerow(data)
		i = i + 1 
		if i%100000==0:
			print 'write %d rows.' % i 
			
	fd.close()	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])