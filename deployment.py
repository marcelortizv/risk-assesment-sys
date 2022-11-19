"""
A Python script that will accomplish model deployment

Author: Marcelo Ortiz
Date: Nov 2022
"""
import os
from shutil import copy2
import json

# Load config.json and correct path variable
with open('config.json', 'r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'])


# function for deployment
def store_model_into_pickle():
    """
    copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file
    into the deployment directory
    :param model:
    :return:
    """
    files = ['ingestedfiles.txt', 'latestscore.txt',
        'trainedmodel.pkl', 'encoder.pkl'
    ]
    for file in files:
        if file == 'ingestedfiles.txt':
            source_path = os.path.join(dataset_csv_path, file)
        else:
            source_path = os.path.join(model_path, file)
        deploy_path = os.path.join(prod_deployment_path, file)
        copy2(source_path, deploy_path)
        print(f'Deploying {source_path} to {deploy_path}')
    print('Deployment done!')


if __name__ == '__main__':
    store_model_into_pickle()
