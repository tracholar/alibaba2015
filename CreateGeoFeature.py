import csv,com,util 
import numpy as np

def IncDict(d, key,k):
	if key in d:
		d[key] = d[key] + 1/k
	else:
		d[key] = 1/k

def GetDict(d, key):
	if key in d:
		return d[key]
	else:
		return 0
	
def getItemGeoDict(d,geo,tid):
	if tid in d:
		if geo not in d[tid]:
			d[tid].append(geo)
	else:
		d[tid] = []
		d[tid].append(geo)
			

def GenFeature(finput='user_action_train.csv',fitem = 'tianchi_mobile_recommend_train_item.csv', foutput = 'feature.csv', lastday = '2014-12-18'):	
	geotree = util.load_obj('geotree')
	
	user_itemgeo_count_before_lastday = dict()
	user_itemgeo_car_before_lastday = dict()
	user_itemgeo_star_before_lastday = dict()
	user_itemgeo_buy_before_lastday = dict()
	user_itemgeo_count_lastday = dict()
	user_itemgeo_car_lastday = dict()
	user_itemgeo_star_lastday = dict()
	user_itemgeo_buy_lastday = dict()	
	
	item_itemgeo = dict()
	
	
	user_count_lastday = dict()
	user_star_lastday = dict()
	user_car_lastday = dict()
	user_buy_lastday = dict()
	user_count_before_lastday = dict()
	user_star_before_lastday = dict()
	user_car_before_lastday = dict()
	user_buy_before_lastday = dict()
	
	user_geocount = dict()
	
	
	
	
		
	user_items = set()
	itemfile = open(fitem,'rb')
	itemreader = csv.reader(itemfile,delimiter = ',')
	
	for row in itemreader:
		tid = row[0]
		if len(row[1]) > 1:
			getItemGeoDict(item_itemgeo,com.GeoMatch(row[1],geotree),tid)
		else:
			item_itemgeo[tid] = []
			item_itemgeo[tid].append(-1)
		#if len(row[1])>1:
			#item_itemgeo[tid] = com.GeoMatch(row[1],geotree)
		#else:
			#item_itemgeo[tid] = -1
	
	
	with open(finput, 'rb') as f:
			reader = csv.reader(f, delimiter=',')
			header = reader.next()
			print header	
	
			i=0
		
			
			for row in reader:
				uid = row[0]
				tid = row[1]
				cid = row[4]				
				
				user_items.add('%s_%s' % (uid,tid))
				
				if tid not in item_itemgeo:
					continue
				
				if item_itemgeo[tid][0] != -1:
					
					
					if row[5][:10] == lastday:
						if row[2] == '1':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_count_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))
						elif row[2] == '2':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_star_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))							
					
						elif row[2] == '3':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_car_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))							
						elif row[2] == '4':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_buy_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))
					else:
						if row[2] == '1':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_count_before_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))
						elif row[2] == '2':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_star_before_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))							
											
						elif row[2] == '3':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_car_before_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))							
						elif row[2] == '4':
							for itemgeohash in item_itemgeo[tid]:
								IncDict(user_itemgeo_buy_before_lastday,'%s_%s' %(uid,itemgeohash),len(item_itemgeo[tid]))						
												
				i = i + 1
				if i % 100000 == 0:
					print 'processed %d scores!' % i
		
		
	fd = open(foutput,'wb')
	fw = csv.writer(fd, delimiter=',')		
		
	fw.writerow(['user_itemgeo_count_before_lastday','user_itemgeo_car_before_lastday','user_itemgeo_star_before_lastday','user_itemgeo_buy_before_lastday','user_itemgeo_count_lastday',
	             'user_itemgeo_car_lastday','user_itemgeo_star_lastday','user_itemgeo_buy_lastday'])
	
	
	for key in user_items:
		uid, tid = key.split('_')

		if tid not in item_itemgeo:
			data = ['','','','','','','','','','']
			continue
		
		if item_itemgeo[tid][0] != -1:
			#data = np.zeros(8)
			temp_count_lastday = 0
			temp_star_lastday = 0
			temp_car_lastday = 0
			temp_buy_lastday = 0
			temp_count_before_lastday = 0
			temp_star_before_lastday = 0
			temp_car_before_lastday = 0
			temp_buy_before_lastday = 0
			for itemgeohash in item_itemgeo[tid]:
				key_uid_itemgeo = '%s_%s' %(uid,itemgeohash)
				#每一个item可能对应多个itemgeo 特征要取均值
				temp_count_lastday += GetDict(user_itemgeo_count_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_star_lastday+= GetDict(user_itemgeo_star_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_car_lastday += GetDict(user_itemgeo_car_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_buy_lastday += GetDict(user_itemgeo_buy_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_count_before_lastday += GetDict(user_itemgeo_car_before_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_star_before_lastday += GetDict(user_itemgeo_star_before_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_car_before_lastday += GetDict(user_itemgeo_car_before_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 
				temp_buy_before_lastday += GetDict(user_itemgeo_buy_before_lastday,key_uid_itemgeo)/len(item_itemgeo[tid]) 	
			data = [uid,tid,
			        temp_count_lastday,
			        temp_star_lastday,
			        temp_car_lastday,
			        temp_buy_lastday,
			        temp_count_before_lastday,
			        temp_star_before_lastday,
			        temp_car_before_lastday,
			        temp_buy_before_lastday]
		fw.writerow(data)
		#else:
			
					
	com.FillAvgData(foutput,'%s_filled.csv' %foutput, log = True)
			
		
		
		
if __name__ == '__main__':
	GenFeature('user_action_train.csv','tianchi_mobile_recommend_train_item.csv','feature.csv','2014-12-18')
		