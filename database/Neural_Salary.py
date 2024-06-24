import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import random_split, TensorDataset
from cleaning_data import df_to_nn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# taking out the variable that we want to predict
data_y = df_to_nn[df_to_nn.columns[5]]

# removing from the dataset variables that doesn´t help us to predict
data_x = df_to_nn.drop(columns=['timestamp', 'job_context', 'annual_salary', 'additional_compensation', 'currency_other', 'income_context','id'])

# Applying one hot encoding to the dataframe in order to the neural network works
data_x = pd.get_dummies(data_x)

scaler = StandardScaler()
data_x = scaler.fit_transform(data_x)

# split the database into a train set and a test set, using sklearn for training using 80% and for test using 20%
X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2, random_state=42)






