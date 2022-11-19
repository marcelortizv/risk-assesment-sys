"""
a script that performs diagnostic tests related to your model as well as your data.

Author: Marcelo Ortiz
Date: Nov 2022
"""
import pandas as pd
import subprocess
import timeit
import os
import json
import sys
from joblib import load
from utils import preprocess_data

# Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])
deploy_path = os.path.join(config['prod_deployment_path'])


# Function to get models predictions
def model_predictions(test_dataset):
    """
    Read the deployed models and a test dataset, calculate predictions
    """
    # load model and encoder
    model = load(os.path.join(deploy_path, "trainedmodel.pkl"))
    encoder = load(os.path.join(deploy_path, "encoder.pkl"))

    # load test data
    if test_dataset is None: test_dataset = "testdata.csv"
    df = pd.read_csv(os.path.join(test_data_path, test_dataset))

    df_x, df_y, _ = preprocess_data(df, encoder)

    y_pred = model.predict(df_x)

    return y_pred, df_y


# Function to get summary statistics
def dataframe_summary(test_dataset):
    """
    Calculate summary statistics
    :return:
    """
    if test_dataset is None: test_dataset = "testdata.csv"
    df = pd.read_csv(os.path.join(test_data_path, test_dataset))

    numeric_columns = [ "lastmonth_activity",
        "lastyear_activity", "number_of_employees"
    ]

    results = []
    for column in numeric_columns:
        results.append([column, "mean", df[column].mean()])
        results.append([column, "median", df[column].median()])
        results.append([column, "standard deviation", df[column].std()])

    return results


# Function to get timings
def execution_time():
    """
    Calculate timing of training.py and ingestion.py
    :return: resuls with computing times
    """
    results = []
    for process in ["training.py", "ingestion.py"]:
        start_time = timeit.default_timer()
        os.system('python3 %s' % process)
        timing = timeit.default_timer() - start_time
        results.append([process, timing])

    return results


# Function to check dependencies
def outdated_packages_list():
    """
    Check dependencies
    :return: a list of updated packages
    """
    outdated_packages = subprocess.check_output(['pip', 'list', '--outdated']).decode(sys.stdout.encoding)

    return str(outdated_packages)


def missing_data(test_dataset):
    """
    calculate number of nans
    :return:
    """
    if test_dataset is None: test_dataset = "testdata.csv"
    df = pd.read_csv(os.path.join(test_data_path, test_dataset))

    results = []
    for column in df.columns:
        count_na = df[column].isna().sum()
        count_not_na = df[column].count()
        count_total = count_not_na + count_na

        results.append([column, str(int(count_na / count_total * 100)) + "%"])

    return results


if __name__ == '__main__':
    model_predictions(None)
    dataframe_summary(None)
    missing_data(None)
    execution_time()
    outdated_packages_list()