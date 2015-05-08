# coding:utf-8

import util, os, sys
from multiprocessing import Pool

if __name__ == '__main__':
	pool = Pool(50)
	root = r'D:\zuoyuan\alibaba\csv'
	fs = util.FilterFile(r'featureTEST_\d+-\d+-\d+\.csv$',root=root)
	cmds = []
	for f in fs:
		cmds.append('python subset.py %s 0,1,2,3,4,5,6' % os.path.join(root,f))
	#print cmds	
	pool.map(os.system, cmds)
	
	