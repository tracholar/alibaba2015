# coding:utf-8
import util

if __name__=='__main__':
	fs = util.FilterFile(r'feature\d*\.csv$')
	for f in fs:
		header = open(f).readline().split(',')
		print f 
		for it in header[2:]:
			print it
		
	
