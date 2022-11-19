"""
a Python script that will accomplish model training

Author: Marcelo Ortiz
Date: Nov 2022
"""

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from utils import preprocess_data
from joblib import dump
import json


# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path']) 


# Function for training the models
def train_model():
    df = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))
    df_x, df_y, encoder = preprocess_data(df, None)

    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.20)
    # use this logistic regression for training
    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                               intercept_scaling=1, l1_ratio=None, max_iter=100,
                               multi_class='ovr', n_jobs=None, penalty='l2',
                               random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                               warm_start=False)
    
    # fit the logistic regression to your data
    model.fit(x_train, y_train)

    # write the trained models to your workspace in a file called trainedmodel.pkl
    dump(model, os.path.join(model_path, "trainedmodel.pkl"))
    dump(encoder, os.path.join(model_path, "encoder.pkl"))


if __name__ == "__main__":
    train_model()
