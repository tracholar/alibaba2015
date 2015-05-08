# coding:utf-8
import csv, sys, com, util
import multiprocessing as mp

from optparse import OptionParser

def GetDict(d, key):
	if key in d:
		return d[key]
	else:
		return 0

def _CombineFeatureLabel(args ):
	f_feature, f_label, f_out = args 
	
	
	f1 = open(f_feature, 'rb')
	fr1 = csv.reader(f1, delimiter=',')

	f2 = open(f_label, 'rb')
	fr2 = csv.reader(f2, delimiter=',')

	f3 = open(f_out, 'wb')
	fw3 = csv.writer(f3, delimiter=',')

	user_item = dict()
	for row in fr2:
		key = '%s_%s' % (row[0],row[1])
		user_item[key] = row[2]
		
	header = fr1.next()
	header.append('buy')
	fw3.writerow(header)

	i = 0
	for row in fr1:
		key = '%s_%s' % (row[0],row[1])
		row.append( GetDict(user_item, key))
		fw3.writerow(row)
		i = i + 1
		if i%100000==0:
			print 'processed %d scores!' % i
			
	f1.close()
	f2.close()
	f3.close()

def CombineFeatureLabel(f_feature, f_label, f_out):
	pool = mp.Pool(com.__n_process)
	
	ffs = ['%s.%d.csv' % (util.file_basename(f_feature),i) for i in range(com.__n_process)]
	fos = ['%s.%d.csv' % (util.file_basename(f_out),i) for i in range(com.__n_process)]
	
	args_list = []
	for i in range(com.__n_process):
		args_list.append((ffs[i],f_label, fos[i]))
		
	pool.map(_CombineFeatureLabel, args_list)
	
	
	
if __name__ == '__main__':
	if sys.argv[1]=='train':
		CombineFeatureLabel('feature.merge.csv','label.csv','data.csv')
	elif sys.argv[1]=='test':
		CombineFeatureLabel('feature_test.merge.csv', 'label_test.csv','data.test.csv')
	else:
		parser = OptionParser()

		parser.add_option('-f','--feature', dest='feature',help='feature file')
		parser.add_option('-l','--label', dest='label',help='label file')
		parser.add_option('-d','--data', dest='data',help='data file')


		(options, args) = parser.parse_args()
		CombineFeatureLabel(options.feature, options.label,options.data)