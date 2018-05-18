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
X = data[['Positive Emotion','Negative Emotion']].values

Y = data['label'].values

regr = linear_model.Ridge (alpha = .5)

# Train the model using the training sets
regr.fit(X, Y)

# Make predictions using the testing set
Y_pred = regr.predict(X)
