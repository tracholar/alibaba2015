# coding:utf-8
import re


s = open('str_format.txt', 'rb').read()

r = re.compile('(\w+)\s*=', re.M)

m = r.findall(s)

print '"' + '",\n"'.join(m) + '"'


for k in m:

	w = k.split('_')
	user = False
	item = False
	cat = False
	ug = False
	
	if 'user' in w:
		user = True
	if 'item' in w:
		item = True
	if 'cat' in w:
		cat = True
	if 'usergeo' in w:
		ug = True
	if user and item:
		key = 'utid'
	elif user and cat:
		key = 'ucid'
	elif item and cat:
		key = 'icid'
	elif item and ug:
		key = 'ugtid'
	elif user:
		key = 'uid'
	elif item:
		key = 'tid'
	elif cat:
		key = 'cid'
	else:
		print 'err'
	print 'GetDict(%s, %s),' % (k, key) 


	
