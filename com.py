# coding:utf-8
import pandas, util, os, pickle
import numpy as np

__n_process = 10

def GetRecItems():
	items = pandas.read_csv('tianchi_mobile_recommend_train_item.csv')
	items = set(items['item_id'])
	return items


def GetBuySet(fn = 'label.csv'):
	data = pandas.read_csv(fn)
	
	s1 = set()
	s2 = set()
	for i in range(len(data)):
		if data['buy'][i]==1:
			s1.add((data['user_id'][i], data['item_id'][i]))
		
	
	return s1
	

def GetItemGeo():
	items = pandas.read_csv('tianchi_mobile_recommend_train_item.csv')
	item_geo = dict()
	for i in range(len(items)):
		tid = items['item_id'][i]
		geo = items['item_geohash'][i]
		
		# print geo, geo is not np.nan
		if geo is not np.nan:
			if tid not in item_geo:
				item_geo[tid] = set()
			
			item_geo[tid].add(geo)
	return item_geo
def GetGeoTree(all = False):
	# print os.path.exists('geotree')
	if os.path.exists('geotree'):
		tree = util.load_obj('geotree')
		return tree
		
	geo_hash = pandas.read_csv('tianchi_mobile_recommend_train_user.csv.subset.csv')
	geo_hash = geo_hash.dropna()
	geo_count=dict()
	
	rule = [(0,0),(1,1e5), (2,1e5),(3,1e5),(4,1e4),(5,1e3),(6,1e3)]
	for r in rule:
		if r[0]==0:
			split_list = ['9','m','f']
			for i in geo_hash['user_geohash']:
				util.IncDict(geo_count, i[:1])
		else:
			split_list=[i for i in geo_count.keys() if geo_count[i]>r[1] and len(i)==r[0] ]
			for i in geo_hash['user_geohash']:
				if i[:r[0]] in split_list:
					util.IncDict(geo_count, i[:r[0]+1])
			

	
	util.save_obj(geo_count, 'geotree')
	if all:
		return geo_count
	else:
		geo_tree = {i:geo_count[i] for i in geo_count.keys() if geo_count[i]>1e5 or len(i)==1}
	return geo_tree
	
def GeoMatch(geo_hash, geo_list):
	geo_set = set(geo_list)
	max_len = max([len(i) for i in geo_set])
	for i in range(max_len,0,-1):
		if geo_hash[:i] in geo_set:
			return geo_hash[:i]

def GeoSamePrefixLen(geo1, geo2):
	assert len(geo1)==len(geo2)
	L = len(geo1)
	for i in range(L):
		if geo1[i]!=geo2[i]:
			break
			
	return i 
	
def GeoDistance(geo1, geo2):
	return len(geo1) - GeoSamePrefixLen(geo1, geo2)

def GeoSetDistance(user_geos, item_geos):  # geo集合的距离，算最短的那个
	d = None
	for i in user_geos:
		for j in item_geos:
			tmp = GeoDistance(i, j) 
			if d is None or tmp < d:
				d = tmp
	return d


def AvgData(fn, log=False):
	block_size = 100000
	fr = pandas.read_csv(fn, iterator=True, chunksize=block_size)

	avg = None
	nrows = 0
	
	rows = 0 
	for data in fr:
		nrows = nrows + len(data)
		rows = rows + np.sum( ~ pandas.isnull(data))
		if log:
			data = np.log(data)
		if avg is None:
			avg = np.sum(data)
		else:
			avg = avg + np.sum(data)
			
		print 'sum %d rows.' % nrows
	
	# assert rows != 0
	
	avg = avg / rows
	if log:
		return np.exp(avg)
	return avg

def FillAvgData(fn, fo, log=False):
	avg = AvgData(fn, log)
	block_size = 100000
	fr = pandas.read_csv(fn, iterator=True, chunksize=block_size)
	
	mod = 'w'
	header = True
		
	nrows = 0
	for data in fr:
		data.fillna(avg).to_csv(fo, mode=mod, header = header,index = False, float_format='%.2e')
		header = False
		mod = 'a'
		
		nrows = nrows + len(data)
		print 'fill %d rows.' % nrows
	
		
def CreateFeature(file, mode):
	fid = util.file_basename_id(file)
	GenFeature = util.load_model_from_name(util.file_basename(file)).GenFeature
	if mode=='train':
		GenFeature('tianchi_mobile_recommend_train_user.csv', 'feature%d.csv' % fid, lastday='2014-12-17')
	if mode=='submit':
		GenFeature('tianchi_mobile_recommend_train_user.csv', 'feature_total%d.csv' % fid, lastday='2014-12-18')
	if mode=='test':
		GenFeature('tianchi_mobile_recommend_train_user.csv', 'feature_test%d.csv' % fid, lastday='2014-12-16')
	
if __name__ == '__main__':
	FillAvgData('feature10.csv','feature10.fill.csv')