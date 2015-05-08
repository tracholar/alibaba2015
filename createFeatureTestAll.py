# coding:utf-8
# all in one
import util,sys, os, re, time
from os import path
from multiprocessing import Pool
import numpy as np

from optparse import OptionParser


def process_f(cmd):
	os.system(cmd)

def FilterFile(s):
	files = [f for f in os.listdir('.') if path.isfile(f) and re.match(s, f) is not None]
	return files
	

if __name__ == '__main__':
	
	parser = OptionParser()

	parser.add_option('-r','--root-dir', default=r'D:\zuoyuan\alibaba\csv\featureTEST', dest='root',help='output data root direction')

	(options, args) = parser.parse_args()
	
	
	pool = Pool(20)

	
	begin = time.mktime(time.strptime('2014-11-18','%Y-%m-%d'))
	end = time.mktime(time.strptime('2014-12-18','%Y-%m-%d'))
	
	cmds = []
	for t in np.arange(begin, end+3600*24, 3600*24):
		t_str = time.strftime('%Y-%m-%d',time.localtime(t))
		cmds.append(r'python createFeatureTest.py -o %s/featureTEST_%s.csv -d %s' % (options.root,t_str,t_str))
		cmds.append(r'python gen_label_data.py -o %s/label_%s.csv -d %s' % (options.root, t_str,t_str))
		
	
	#for c in cmds:
	#	print c 
	pool.map(process_f, cmds)
	
	
	
	
	
	

