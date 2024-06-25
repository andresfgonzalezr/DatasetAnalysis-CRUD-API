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


# print('x Train: {}, x Test: {}, y Train: {}, y Test: {}'.format(X_train.shape, X_test.shape, y_train.shape, y_test.shape))
y_train = y_train.astype(float)
y_test = y_test.astype(float)


n_entries = X_train.shape[1]
# print(n_entries)

tensor_X_train = torch.tensor(X_train, dtype=torch.float32).to('cpu')
tensor_X_test = torch.tensor(X_test, dtype=torch.float32).to('cpu')
tensor_y_train = torch.tensor(y_train.values, dtype=torch.float32).to('cpu')
tensor_y_test = torch.tensor(y_test.values, dtype=torch.float32).to('cpu')
tensor_y_train = tensor_y_train[:,None]
tensor_y_test = tensor_y_test[:,None]

# test = TensorDataset(tensor_X_train, tensor_y_train)


class NeuralSalary(nn.Module):
    def __init__(self, n_entries):
        super(NeuralSalary, self).__init__()
        self.Linear1 = nn.Linear(n_entries, 6000)
        self.Linear2 = nn.Linear(6000, 3000)
        self.Linear3 = nn.Linear(3000, 1000)
        self.Linear4 = nn.Linear(1000, n_entries)

    def forward(self, inputs):
        prediction1 = torch.sigmoid(input=self.Linear1(inputs))
        prediction2 = torch.sigmoid(input=self.Linear2(prediction1))
        prediction3 = torch.sigmoid(input=self.Linear3(prediction2))
        prediction_f = torch.sigmoid(input=self.Linear4(prediction3))

        return prediction_f






