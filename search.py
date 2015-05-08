# coding:utf-8
import csv,sys

f = open('tianchi_mobile_recommend_train_user.csv', 'rb')
fr = csv.reader(f, delimiter=',')

assert len(sys.argv)==3
uid = sys.argv[1]
tid = sys.argv[2]

fd = open('%s_%s.csv' % (uid, tid), 'wb')
fw = csv.writer(fd, delimiter=',')

fw.writerow(fr.next())

nrows = 0 
rows = 0
for row in fr:
	if row[0] == uid and row[1] == tid:
		fw.writerow(row)
		print row
		nrows = nrows + 1
	rows = rows + 1
	if rows%100000==0:
		print 'process %d rows.' % rows
print 'find %d rows.' % nrows
fd.close()
f.close()

	

