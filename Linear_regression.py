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

data = pd.read_csv('Get_LIWC.csv')

x =data[['Positive Emotion','Negative Emotion','Anxiety','Anger','Death','Feel','Health']].values
#print(x)
print(x.shape)
#
target = pd.read_csv('dataset_lable.csv')
y =target['lable'].values
#print(y)
print(y.shape)
#
#
#convert to array to fit the model
x=np.asarray(x)
y=np.asarray(y)

# print(x)
# print(y)

# Split the data into training/testing sets
diabetes_X_train = x[:800] # 100 aval
diabetes_X_test = x[-100:]  #100 akhar

# Split the targets into training/testing sets
diabetes_y_train = y[:800]
diabetes_y_test = y[-100:]

regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train, diabetes_y_train)


diabetes_y_pred = regr.predict(diabetes_X_test)
#print(diabetes_y_pred)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))