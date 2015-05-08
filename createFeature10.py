# coding:utf-8

import csv, time,sys, util, com
import numpy as np



# 特征生成文件10, item geo feature
# 

usergeo_item_lastday_click = dict()
usergeo_item_lastday_star = dict()
usergeo_item_lastday_cart = dict()
usergeo_item_lastday_buy = dict()

usergeo_item_before_lastday_click = dict()
usergeo_item_before_lastday_star = dict()
usergeo_item_before_lastday_cart = dict()
usergeo_item_before_lastday_buy = dict()

user_item_geo_distance = dict()

user_item_geo_avg_distance = ''  # 平均距离，用户填充，后面会精确计算这个平均距离
item_geohashs = com.GetItemGeo()
user_geohashs = dict()

geo_ids = set()
geo_list = com.GetGeoTree().keys()
user_geos = dict()

geo_uids = dict()



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
				
			i = i + 1
			
			
			if i%100000==0:
				#break
				print 'processed %d scores!' % i
				
				
				
			uid = row[0]
			tid = row[1]
			cid = row[4]
			t = row[5]
			behavior = row[2]
			
			utid = '%s_%s' % (uid, tid)
			ucid = '%s_%s' % (uid, cid)
			
			user_items.add('%s_%s' % (uid,tid))
			item_cat[tid] = cid
			
			
			
			geo_hash = row[3]
			if geo_hash is np.nan or geo_hash is '':
				continue
			
			util.AddToSetInDict(user_geohashs, uid, geo_hash)
		
			geo_id = com.GeoMatch(geo_hash, geo_list)
			ugtid = 'geo_%s_%s' % (geo_id, tid)
			
			if geo_id not in geo_uids:
				geo_uids[geo_id] = set()
			geo_uids[geo_id].add(uid)
			
			if uid not in user_geos:
				user_geos[uid] = set()
			user_geos[uid].add(geo_id)
			
			if row[5][:10]==lastday:  # lastday
				if row[2] == '1': # click
					IncDict(usergeo_item_lastday_click, ugtid)
				elif row[2] == '2': # star
					IncDict(usergeo_item_lastday_star, ugtid)
				elif row[2] == '3': # add to car
					IncDict(usergeo_item_lastday_cart, ugtid)
				elif row[2] == '4':  # buy
					IncDict(usergeo_item_lastday_buy, ugtid)
			
			else:
				
				if row[2] == '1': # click
					IncDict(usergeo_item_before_lastday_click, ugtid)
				elif row[2] == '2': # star
					IncDict(usergeo_item_before_lastday_star, ugtid)
				elif row[2] == '3': # add to car
					IncDict(usergeo_item_before_lastday_cart, ugtid)
				elif row[2] == '4':  # buy
					IncDict(usergeo_item_before_lastday_buy, ugtid)
				
			
	
	
			
	# user feature
	fd = open('%s.tmp.csv' % foutput,'wb')
	fw = csv.writer(fd, delimiter=',')

	fw.writerow(['user_id', 'item_id',
		"usergeo_item_lastday_click",
		"usergeo_item_lastday_star",
		"usergeo_item_lastday_cart",
		"usergeo_item_lastday_buy",
		"usergeo_item_before_lastday_click",
		"usergeo_item_before_lastday_star",
		"usergeo_item_before_lastday_cart",
		"usergeo_item_before_lastday_buy",
		
		"geo_users_number",
		"user_item_geo_distance"
		
	] )
	
	avggeodata = ['', '', '', '', '', '', '', '' ]
	
	i = 0
	for key in user_items:
		uid, tid = key.split('_')
		cid = item_cat[tid]
		utid = '%s_%s' % (uid, tid)
		ucid = '%s_%s' % (uid, cid)
			
		users_number = ''
		
		if uid not in user_geos:  # 没有用户位置信息的用平均值填充
			# print uid
			geodata = avggeodata
		else:		
			geodata = np.zeros(8)
			
			users_number = 0 
			
			for geo_id in user_geos[uid]:
				ugtid = 'geo_%s_%s' % (geo_id, tid)
				
				if geo_id in geo_uids:
					users_number = users_number + len(geo_uids[geo_id])
			
				
				tmp = [
					GetDict(usergeo_item_lastday_click, ugtid),
					GetDict(usergeo_item_lastday_star, ugtid),
					GetDict(usergeo_item_lastday_cart, ugtid),
					GetDict(usergeo_item_lastday_buy, ugtid),
					GetDict(usergeo_item_before_lastday_click, ugtid),
					GetDict(usergeo_item_before_lastday_star, ugtid),
					GetDict(usergeo_item_before_lastday_cart, ugtid),
					GetDict(usergeo_item_before_lastday_buy, ugtid),
				]
				geodata = geodata + (np.array(tmp) + 1.0/len(geo_list)) / len(geo_uids[geo_id])  # 去除0均值
				
			
			geodata = geodata / len(user_geos[uid]) 
			geodata = ['%.2e' % d for d in geodata]
			
			users_number = float(users_number) / len(user_geos[uid])
		
		# user item geo distance
		#print uid not in user_geohashs or int(tid) not in item_geohashs
		if uid not in user_geohashs or int(tid) not in item_geohashs:
			geo_distance = user_item_geo_avg_distance
		else:
			#print 'got here!', (user_geohashs[uid], item_geohashs[int(tid)])
			geo_distance = com.GeoSetDistance(user_geohashs[uid], item_geohashs[int(tid)])
			
		
		
		data = [uid, tid,
	
			] + geodata + [users_number, geo_distance]
		
		fw.writerow(data)
		
		i = i + 1 
		if i%100000==0:
			print 'write %d rows to file.' % i
		
	fd.close()	

	com.FillAvgData('%s.tmp.csv' % foutput, foutput, log=True)  # 将空值用均值填充
	


if __name__ == '__main__':
	com.CreateFeature(__file__, sys.argv[1])