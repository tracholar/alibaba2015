# coding:utf-8
'''


'''
import csv,sys,os
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s','--sort',action="store_true", default=False, dest='s',help='sort result')
parser.add_option('-n','--number',action="store_true", default=False, dest='n',help='show number')
parser.add_option('-f','--format',action="store_true", default=False, dest='f',help='format to copy')


(options, args) = parser.parse_args()


if len(args)<1:

	fn = 'data.train.csv'
else:
	fn = args[0]
f = open(fn,'rb')
fr = csv.reader(f, delimiter=',')

header = fr.next()
f.close()
if options.s:
	header.sort()
print 'File: %s\n' % fn
for i in range(len(header)):
	if options.n:
		print i, header[i]
	elif options.f:
		print '"%s",' % header[i]
	else:
		print header[i]
	
