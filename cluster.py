# coding:utf-8
# cluster


import pandas as pd
import numpy as np
from sklearn.lda import LDA
from sklearn.decomposition import PCA
from matplotlib.pyplot import *
from sklearn.preprocessing import Normalizer, MinMaxScaler,StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

def Cluster(data,n_clusters = 5,pca_components=5):
	
	cluster = KMeans(n_clusters=n_clusters)
	scaler = StandardScaler()

	pca = PCA(n_components=pca_components)

	pipetr = Pipeline([('scaler',scaler),('pca',pca)])
	pipe = Pipeline([('tr', pipetr),('cluster',cluster)])
	pipe.fit(data)
	
	X = pipetr.transform(data)
	Y = pipe.predict(data)
	

	color=cm.rainbow(np.linspace(0,1,n_clusters))
	for i in range(n_clusters):
		scatter(X[Y==i,0],X[Y==i,1],c=color[i])
		
	show()
	
	
if __name__ == '__main__':
	data = pd.read_csv('data.train.csv')
	Cluster(data)
	
	