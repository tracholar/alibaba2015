# coding:utf-8
# all in one
import util,sys, os, re
from os import path
from multiprocessing import Pool


def process_f(cmd):
	os.system(cmd)

def FilterFile(s):
	files = [f for f in os.listdir('.') if path.isfile(f) and re.match(s, f) is not None]
	return files
	

if __name__ == '__main__':
	if len(sys.argv)==1:
		model_name = 'model0'
	else:
		model_name = sys.argv[1]
	pool = Pool(20)

	

	createfeature_fileset = FilterFile(r'createFeature\d*\.py$')
	cmds = ["python %s train" % f for f in createfeature_fileset]
	cmds = cmds + ["python %s submit" % f for f in createfeature_fileset]
	cmds = cmds + ["python %s test" % f for f in createfeature_fileset]
	cmds = cmds + ['python gen_label_data.py train', 'python gen_label_data.py test']
	
	pool.map(process_f, cmds)
	
	print 'createFeature done!'
	
	
	
	cmds = ['python merge_fast.py train',
			'python merge_fast.py test',
			'python merge_fast.py submit']
	pool.map(process_f, cmds)
	
	print 'merge feature done!'
	
	pool.map(process_f, ['python gen_data.py train', 'python gen_data.py test'])
	
#	pool.map(process_f, ['python filter.py %s' % s for s  in ['train','test','submit'] ])
	
	os.system('python data_sample.py train')
	
	print 'gen data done!'
	
	#models = FilterFile(r'model\d*.py$')
	#cmds = ['python %s'%  f for f in models]
	#pool.map(process_f, cmds)
	os.system('python %s.py' % model_name)
	
	print 'train model done!'
	
	os.system('python gen_rec_data.py %s' % model_name)
	
	print 'gen recomannd data done!'
	
	print 'god done!'
	
	
	
	

