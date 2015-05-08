# coding:utf-8

import csv, sys, util, random

from optparse import OptionParser

parser = OptionParser()


parser.add_option('-n','--number', default=10000, dest='count',help='sample number')
parser.add_option('-p','--prob', type='float', dest='p',help='sample probability')
#parser.add_option('-f','--file', dest='fname',help='file name to sample')

(options, args) = parser.parse_args()
#print options,args
#sys.exit()

fname = util.file_basename(args[0])
fd = open('%s.sample.csv' % fname,'wb')
writer = csv.writer(fd, delimiter=',')
with open('%s.csv' % fname, 'rb') as f:
	reader = csv.reader(f, delimiter=',')
	i = 0
	
	for row in reader:
	
		if i==0 or options.p is None or random.random()<options.p:
			writer.writerow(row)
		
			
		
		i = i+1
		if options.p is None and i==options.count:
			break
		if i%100000==0:
			print 'process %d rows.' % i
fd.close()