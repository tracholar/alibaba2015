# coding:utf-8
import csv

fd1 = open('user_action_train.csv', 'wb')
fwr1 = csv.writer(fd1, delimiter=',')

fd2 = open('user_action_test.csv', 'wb')
fwr2 = csv.writer(fd2, delimiter=',')


f = open('tianchi_mobile_recommend_train_user.csv', 'rb')
fr = csv.reader(f, delimiter=',')
# header
header = fr.next()
fwr1.writerow(header)
fwr2.writerow(header)

i = 0
for row in fr:
	# filter 2014-12-18
	if row[5][:10]=='2014-12-18':
		fwr2.writerow(row)
	else:
		fwr1.writerow(row)
	
	i = i + 1
	if i%100000==0:
		print 'processed %d scores!' % i
fd1.close()
fd2.close()