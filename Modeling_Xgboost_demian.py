import torch
torch.cuda.is_available()
 
from google.colab import auth
auth.authenticate_user()

from google.colab import drive
drive.mount('/content/gdrive')

import pickle
from sklearn.model_selection import train_test_split
import xgboost as xgb
from datetime import datetime
import pandas as pd

train_set, test_set = train_test_split( raw , test_size=0.3, random_state=42)

train_y = train_set['y']
train_X = train_set.drop(['y'], axis = 1)

test_y = test_set['y']
test_X = test_set.drop(['y'], axis = 1)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
train_X = scaler.fit_transform(train_X)
test_X = scaler.fit_transform(test_X)

from xgboost import XGBClassifier
import numpy as np
import matplotlib.pyplot as plt

X, y = train_X, train_y

from sklearn.model_selection import validation_curve

# tuning hyper parameters
# hidden_layer_sizes
# Create range of values for parameter

def search(name,param_range):

  # Calculate accuracy on training and test set using range of parameter values
  train_scores, test_scores = validation_curve(XGBClassifier(random_state = 201310299,tree_method='gpu_hist'), 
                                               X, 
                                               y, 
                                               param_name= name, 
                                               param_range=param_range,
                                               cv=3, 
                                               scoring="accuracy", 
                                               n_jobs=-1)

  # Calculate mean and standard deviation for training set scores
  train_mean = np.mean(train_scores, axis=1)
  train_std = np.std(train_scores, axis=1)

  # Calculate mean and standard deviation for test set scores
  test_mean = np.mean(test_scores, axis=1)
  test_std = np.std(test_scores, axis=1)

  # Plot mean accuracy scores for training and test sets
  plt.plot(param_range, train_mean, label="Training score", color="black")
  plt.plot(param_range, test_mean, label="Cross-validation score", color="dimgrey")

  # Plot accurancy bands for training and test sets
  plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, color="gray")
  plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, color="gainsboro")

  # Create plot
  plt.title("Validation Curve With XGB")
  plt.xlabel("parameter value")
  plt.ylabel("Accuracy Score")
  plt.tight_layout()
  plt.legend(loc="best")
  plt.show()

search('min_child_weight',np.arange(1,10,2))
search('gamma',np.arange(0.5,3,0.5))
search('subsample',np.arange(0.6,1.2,0.2))
search('colsample_bytree',np.arange(0.6,1,0.2))
search('max_depth',np.arange(3,15,1))
search('eta',[0.01,0.05,0.1,0.3,0.5,0.7])
search('n_estimators',np.arange(100,2300,100))
search('base_score',np.arange(0.1,1,0.1))

start = datetime.now()
gbm = xgb.XGBClassifier(n_estimator = 40,min_samples_leaf=3, tree_method = 'gpu_hist').fit(train_X, train_y)
predictions = gbm.predict(test_X)
end = datetime.now()

sum(test_y == predictions)/len(predictions)

dict(zip(gbm.feature_importances_,list(X)))