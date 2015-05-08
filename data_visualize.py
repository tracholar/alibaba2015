# coding:utf-8
from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from model15 import GetData

X,Y = GetData()

m = np.cov(X)

print m