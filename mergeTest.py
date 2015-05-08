# coding:utf-8
import os, sys, util


root = r'D:\zuoyuan\alibaba\csv'
fs = util.FilterFile(r'feature.+subset_0_1_2_3_4_5_6\.csv$',root=root)

for f in fs:
	print f 
	
sys.exit()
cmd = 'python merge_fast.py ' +  ' '.join([os.path.join(root,f) for f in fs]) + ' ' + os.path.join(root,'feature_0_1_2_3_4_5_6.csv')
os.system(cmd)



