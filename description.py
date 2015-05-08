# coding:utf-8
'''
description of data
usage: description.py data.csv
'''

import com, util
import pandas
import numpy as np

block_size = 10000
fr = pandas.read_csv('feature_total.merge.csv', iterator=True, chunksize=block_size)

nrows = 0
for data in fr:
	