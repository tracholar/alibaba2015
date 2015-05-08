# coding:utf-8
from sklearn.base import BaseEstimator
import model16, model14

class Mode9216(BaseEstimator):
	
	def __init__(self,C=1.,class_weight=[]):
		self.m16 = model16.GetModel()
		self.m92 = model14.GetModel()
	
	def fit(self, X, Y=None):
		pass
	
	def predict(self, X, th=0.5):
		return (self.predict_proba(X)[:,1]>th).astype(int)
		
	def predict_proba(self, X):
		k = 0.7
		offset = 0.03
		return self.m16.predict_proba(X[model16._feature_names]) * k+ self.m92.predict_proba(X[model14._feature_names])*(1-k) + offset
