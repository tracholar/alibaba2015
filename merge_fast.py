# coding:utf-8
import csv, sys, pandas, util, re, com
import numpy as np

def KEY(s):
	if re.search(r'\d+', s):
		return int(re.search(r'\d+', s).group()) 
	else: 
		return 0 
if len(sys.argv)==2:
	# merge all 
	if sys.argv[1]=='train':
		fs = util.FilterFile(r'feature\d*.csv$')
		fo = 'feature.merge.csv'
	elif sys.argv[1]=='submit':
		fs = util.FilterFile(r'feature_total\d*.csv$')
		fo = 'feature_total.merge.csv'
	elif sys.argv[1]=='test':
		fs = util.FilterFile(r'feature_test\d*.csv$')
		fo = 'feature_test.merge.csv'
	else:
		sys.exit()
	sys.argv.pop()
	fs.sort(key = KEY)
	print 'merge files:'
	for f in fs:
		sys.argv.append(f)
		print f
	print 
	sys.argv.append(fo)
	
elif len(sys.argv)<4:
	print 'usage  python merge_fast.py [f1 ... fn fo]'
	sys.exit()
	
f = []
fr = []

fns = len(sys.argv)-2
for i in range(1,fns+1):
	fd = open(sys.argv[i],'rb')
	f.append(fd)
	reader = csv.reader(fd, delimiter=',')
	fr.append(reader)


fo = sys.argv[-1]
fo_base = util.file_basename(fo)
fo_list = [open('%s.%d.csv' % (fo_base, j),'wb' ) for j in range(com.__n_process)]
fw_list = [csv.writer(fo, delimiter=',') for fo in fo_list]
fidx = 0

header = fr[0].next()
for i in range(1,fns):
	header = header + fr[i].next()[2:]

map(lambda fw: fw.writerow(header), fw_list) # write header

nrows = 0
for row in fr[0]:
	for i in range(1,fns):
		newdata = fr[i].next()
		if (row[0]!=newdata[0] or row[1]!=newdata[1]):
			print 'key error happen at %d row.' % (nrows+1)
			sys.exit()
		row = row + newdata[2:]
	
	fw_list[fidx].writerow(row)
	fidx = (fidx+1) % com.__n_process
	
	nrows = nrows + 1
	if nrows%100000==0:
		print 'processed %d rows.' % nrows

for i in range(fns):
	f[i].close()

map(lambda fo: fo.close(), fo_list)

