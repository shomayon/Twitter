print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause


import matplotlib.pyplot as plt
import numpy as np
from sklearn import  linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
#from sklearn.model_selection import KFold
#from sklearn.model_selection import cross_val_predict

#import matplotlib.pyplot as plt

data = pd.read_csv('Get_LIWC_240.csv')

x =data[['Positive Emotion','Negative Emotion']].values
#print(x)
#print(x.shape)

target = pd.read_csv('shidehtest.csv')
y =target['lable'].values
#print(y)
#print(y.shape)

#
 #convert to array to fit the model
x=np.asarray(x)
y=np.asarray(y)

# print(x)
# print(y)

# Split the data into training/testing sets
diabetes_X_train = x[:100] # 100 aval
diabetes_X_test = x[-100:]  #100 akhar

# Split the targets into training/testing sets
diabetes_y_train = y[:100]
diabetes_y_test = y[-100:]

regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train, diabetes_y_train)


diabetes_y_pred = regr.predict(diabetes_X_test)
print(diabetes_y_pred)