# coding:utf-8
'''
gen_label_data.py [train|test]
'''
import csv,sys
from optparse import OptionParser


if sys.argv[1]=='train':
	fn = 'label.csv'
	day = '2014-12-18'
elif sys.argv[1]=='test':
	fn = 'label_test.csv'
	day = '2014-12-17'
else:
	parser = OptionParser()

	parser.add_option('-o','--out', dest='fn',help='label file to write')
	parser.add_option('-d','--day', dest='day',help='day')
	(options, args) = parser.parse_args()
	
	fn = options.fn 
	day = options.day
	if fn is None or day is None:
		print __doc__
		sys.exit()
	
f = open('tianchi_mobile_recommend_train_user.csv', 'rb')
fr = csv.reader(f, delimiter=',')

fd = open(fn, 'wb')
fw = csv.writer(fd, delimiter=',')

fr.next()
fw.writerow(['user_id', 'item_id', 'buy'])

user_item_buy = dict()

i = 0
for row in fr:
	i = i + 1
	if i%100000==0:
		print 'process %d rows.' % i
	if row[5][:len(day)]!=day:
		continue
	key = '%s_%s' % (row[0], row[1])
	
	
	if row[2] == '4':
		user_item_buy[key] = 1
	#elif key not in user_item_buy:
	#	user_item_buy[key] = 0


		
for key, value in user_item_buy.items():
	uid, tid = key.split('_')
	data = [uid, tid, value]
		
	fw.writerow(data)
		

f.close()
fd.close()