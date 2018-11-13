from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import numpy as np
import pandas as pd

data = pd.read_csv('dataset_features.csv')

X = data[['Positive Emotion','Negative Emotion','Anxiety','Anger','Death','Feel','Health','Articles',
         'Auxiliary Verbs','Conjunctions','Adverbs','Personal Pronouns',
         'function','Assent','Certainty']].values

Y = pd.read_csv('labeled_tweets.csv')['label'].values

num_folds = 10
C_values = np.logspace(-4,2,10)
accu_val = np.zeros((len(C_values),num_folds))

kf = KFold(n_splits=num_folds)

fold = 0
for train_index, val_index in kf.split(X):
    x_train, y_train = X[train_index,:], Y[train_index]
    x_val, y_val = X[val_index,:], Y[val_index]
    for i, c in enumerate(C_values):
        clf = LogisticRegression(solver='lbfgs', multi_class='multinomial',C=c).fit(x_train, y_train)
        pred = clf.predict(x_val)
        accu_val[fold,i] = np.mean(pred==y_val)
    fold += 1

C_best = C_values[np.argmax(np.mean(accu_val,axis=0))]

data_test = pd.read_csv('dataset_features_test.csv')

X_test = data_test[['Positive Emotion','Negative Emotion','Anxiety','Anger','Death','Feel','Health','Articles',
              'Auxiliary Verbs','Conjunctions','Adverbs','Personal Pronouns',
              'function','Assent','Certainty']].values

clf = LogisticRegression(solver='lbfgs', multi_class='multinomial',C=C_best).fit(X, Y)

pred_test = clf.predict(X_test)

infname = '/Users/shideh/PycharmProjects/untitled5/SentimentAnalyzer3/DATA/merged/Merged_all_fornow.csv'
tweets = pd.read_csv(infname, engine='python')
# print(tweets)
tweets['label'] = pred_test
tweets.to_csv('prediction_tweets.csv',  index=False, columns = ['label','text'])
# out_file = open('predicted_tweets.csv','w')
# with open(infname,'r') as fid:
#     for i, line in enumerate(fid):
#         out_file.write(str(pred_test[i]) + ', ' + line + '\n')
# out_file.close()
