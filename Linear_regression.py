print(__doc__)


import matplotlib.pyplot as plt
import numpy as np
from sklearn import  linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import csv
#from sklearn.model_selection import KFold
#from sklearn.model_selection import cross_val_predict

#import matplotlib.pyplot as plt

data = pd.read_csv('dataset_features.csv')

x =data[['Positive Emotion','Negative Emotion','Anxiety','Anger','Death','Feel','Health','Articles',
         'Auxiliary Verbs','Conjunctions','Adverbs','Personal Pronouns',
        'function','Assent','Certainty']].values
#print(x)
print('x shape:',x.shape)
#
target = pd.read_csv('labeled_tweets.csv')
y =target['lable'].values
#print(y)
print('y shape:', y.shape)
#
#
#convert to array to fit the model
x=np.asarray(x)
y=np.asarray(y)

# print(x)
# print(y)

n = x.shape[0]
n_train = int(np.round(n * 0.9))
n_valid = n - n_train

idx = np.random.permutation(n)
x = x[idx,:]
y = y[idx]

# Split the data into training/testing sets
diabetes_X_train = x[:n_train,:] #
diabetes_X_test = x[n_train:, :]  #

print('train X:',diabetes_X_train.shape)
print('test X:',diabetes_X_test.shape)

# Split the targets into training/testing sets
diabetes_y_train = y[:n_train]
diabetes_y_test = y[n_train:]

print('train target:',diabetes_y_train.shape)
print('test target:',diabetes_y_test.shape)
#print(diabetes_X_train.shape)
#print(diabetes_y_train.shape)
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

data = pd.read_csv('dataset_features_test.csv')

x_test =data[['Positive Emotion','Negative Emotion','Anxiety','Anger','Death','Feel','Health','Articles',
         'Auxiliary Verbs','Conjunctions','Adverbs','Personal Pronouns',
         'function','Assent','Certainty']].values


pred = regr.predict(x_test)

infname='SentimentAnalyzer3/DATA/merged/Merged_all_fornow.csv'
tweets = pd.read_csv(infname)
# print(tweets)
tweets['label'] = pred
tweets.to_csv('prediction_tweets.csv',  index=False, columns = ['label','text'])

