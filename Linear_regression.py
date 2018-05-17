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

# Load the diabetes dataset
#diabetes = datasets.load_diabetes()
x = data[:1]
y = data['col43']

#convert to array to fit the model
x=np.asarray(x)
y=np.asarray(y)

regr = linear_model.LinearRegression()
regr.fit(x, y)

y_predicted = regr.predict(x)

plt.scatter(x, y,  color='black')
plt.plot(x, y_predicted, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()