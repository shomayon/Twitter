
import matplotlib.pyplot as plt
import numpy as np
from sklearn import  linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd



data = pd.read_csv('Get_LIWC_1000.csv')
target = pd.read_csv('shidehtest.csv')
# x,y bezaram too matrix 2- peyda konam chejori ye col ke mikham begiram 3- x 250 *2 - x addae 1 ro be matrix ezafe mikone

x =data[['Positive Emotion','Negative Emotion']].values
target = pd.read_csv('shidehtest.csv')
y =target['lable'].values

def predict(self, X):
        x = self._add_ones_to(X)
#
        return x.dot(self.beta)

def fit(self, X, y):
        x = self._add_ones_to(X)

        self.beta = np.linalg.inv(np.dot(x.T, x)).dot(x.T).dot(y)

def _add_ones_to(self, X):
        n, dim = X.shape
        x = np.ones([n, dim+1])
        x[: , 1: ] = X

        return x