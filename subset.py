# coding: utf-8
''' 
take subset of data
usage: subset.py filename 1,2,3,4
'''

import csv, sys, util

if len(sys.argv)!=3:
	print __doc__
else:
	cols = [int(i) for i in sys.argv[2].split(',')]
	f = open(sys.argv[1], 'rb')
	fr = csv.reader(f, delimiter=',')
	
	fd = open('%s.subset_%s.csv' % (util.file_basename(sys.argv[1]), '_'.join([str(i) for i in cols])), 'wb')
	fw = csv.writer(fd, delimiter=',')
	
	nrows = 0
	for row in fr:
		fw.writerow([row[i] for i in cols])
		nrows = nrows + 1
		if nrows%100000==0:
			print 'processed %d rows!' % nrows
	
	f.close()
	fd.close()
	
	

