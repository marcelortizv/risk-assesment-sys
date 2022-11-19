"""
This script perform data ingestion

Author: Marcelo Ortiz
"""
import pandas as pd
import glob
import os
import json


# Load config.json and get input and output paths
with open('config.json', 'r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']


# Function for data ingestion
def merge_multiple_dataframe():
    """
    check for datasets, compile them together,
    and write to an output file
    """
    # check all csv files in directory
    csv_files = glob.glob("%s/*.csv" % input_folder_path)
    # read all csv files
    df = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)
    # drop duplicates
    df.drop_duplicates(inplace=True)
    # save final data
    df.to_csv("%s/finaldata.csv" % output_folder_path, index=False)

    with open(os.path.join(output_folder_path, "ingestedfiles.txt"), "w") as report_file:
        for line in csv_files:
            report_file.write(line + "\n")


if __name__ == '__main__':
    merge_multiple_dataframe()
