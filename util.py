# coding:utf-8
# util
import imp, smtplib, os, re, time, pickle
from email.mime.text import MIMEText
from os import path
import numpy as np

__send_email = False

def FilterFile(s,root='.'):
	files = [f for f in os.listdir(root) if path.isfile(path.join(root,f)) and re.match(s, f) is not None]
	return files
	
def file_basename(fn):
	# fname = path.join([os.path.dirname(fn) , os.path.basename(fn)])
	fname = fn[:fn.rindex('.')]
	return fname
def file_basename_id(fn):
	fname = file_basename(fn)
	fid = re.search('\d+', fname)
	if fid is None:
		return 1

	return int(fid.group())
	
	
def IncDict(d, key):
	if key in d:
		d[key] = d[key] + 1
	else:
		d[key] = 1

def GetDict(d, key):
	if key in d:
		return d[key]
	else:
		return 0
def AddToSetInDict(d, key, v):
	''' append value to dict with key = key '''
	if key not in d:
		d[key] = set()
	d[key].add(v)
def GetSetFromDict(d, key):
	if key not in d:
		return set()
	return d[key]
	

def DiffTime(t1, t2):
	t1 = time.mktime(time.strptime(t1,'%Y-%m-%d %H'))
	t2 = time.mktime(time.strptime(t2,'%Y-%m-%d %H'))
	return t1 - t2
def MakeDateList(begin, end):
	
	begin = time.mktime(time.strptime(begin,'%Y-%m-%d'))
	end = time.mktime(time.strptime(end,'%Y-%m-%d'))
	
	for t in np.arange(begin, end+3600*24, 3600*24):
		yield(time.strftime('%Y-%m-%d',time.localtime(t)))
	
def load_model_from_name(name):
	
	fp, pathname, description = imp.find_module(name)
	return imp.load_module(name, fp, pathname, description)
	
def send_email(title, email_str):
	if __send_email==False:
		return
	msg = MIMEText(email_str.encode('utf-8'), 'html', 'utf-8')
	msg['Subject'] = title.encode('utf-8')
	msg['From'] = 'tracholar_devtest@163.com'
	msg['To'] = '563876960@qq.com'

	try:
		s = smtplib.SMTP('smtp.163.com')
		pw = open('pw.pw','rb').read()
		
		s.login('tracholar_devtest@163.com',pw)
	
		s.sendmail(msg['From'], ['15155977600@139.com', '563876960@qq.com'], msg.as_string())
		s.quit()
	except Exception:
		print 'Can not send email.'
	
	
		
def notify_me(msg):
	send_email(msg, msg)
def save_obj(obj, fn):
	f = open(fn, 'wb')
	pickle.dump(obj, f)
	f.close()
def load_obj(fn):
	f = open(fn, 'rb')
	obj = pickle.load(f)
	f.close()
	return obj

def LastNDay(day, n):
	return time.strftime('%Y-%m-%d %H', time.localtime(time.mktime(time.strptime('%s 00' % day[:10],'%Y-%m-%d %H')) - (n-1)*24*3600))
def LastWeek(day):
	return time.strftime('%Y-%m-%d %H', time.localtime(time.mktime(time.strptime('%s 00' % day[:10],'%Y-%m-%d %H')) - 6*24*3600))
def HalfMonth(day):
	return time.strftime('%Y-%m-%d %H', time.localtime(time.mktime(time.strptime('%s 00' % day[:10],'%Y-%m-%d %H')) - 14*24*3600))

def GetFeatureNames():
	s = open('features.txt').read()
	s = re.sub(r'//[^\n\r]*', '', s)
	fs = [i.strip() for i in s.replace('"','').split(',') if i.strip() is not '']
	return fs
	
if __name__ == '__main__':
	print GetFeatureNames()