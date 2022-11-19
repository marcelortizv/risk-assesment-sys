"""
automate the ML model scoring and monitoring process.

Author: Marcelo Ortiz
Date: Nov 2022
"""

import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting
import json
import os

# Check and read new data
with open("config.json", "r") as f:
    config = json.load(f)

input_folder_path = config["input_folder_path"]
prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'])

ingested_files = []
with open(os.path.join(prod_deployment_path, "ingestedfiles.txt"), "r") as report_file:
    for line in report_file:
        ingested_files.append(line.rstrip())

# determine whether the source data folder has files that aren't listed in ingestedfiles.txt
new_data = False
for file in os.listdir(input_folder_path):
    filename = input_folder_path + "/" + file
    if filename not in ingested_files:
        new_data = True

if not new_data:
    print("No new ingested data, exiting")
    exit(0)

# perform data ingestion
ingestion.merge_multiple_dataframe()

# scoring
scoring.score_model(production=True)

# retrieve f1 score of deployed model
with open(os.path.join(prod_deployment_path, "latestscore.txt"), "r") as report_file:
    old_f1 = float(report_file.read())

# retrieve f1 score of new model
with open(os.path.join(model_path, "latestscore.txt"), "r") as report_file:
    new_f1 = float(report_file.read())

# Checking for models drift
if new_f1 >= old_f1:
    print("Current F1 score (%s) is better/equal than old F1 score (%s), no drift detected -> exiting" % (new_f1, old_f1))
    exit(0)

# Deciding whether to proceed, part 2
# if you found models drift, you should proceed. otherwise, do end the process here
print("Current F1 score (%s) is worse than old F1 score (%s), drift detected -> training model" % (new_f1, old_f1))
training.train_model()

# Re-deployment
# if you found evidence for models drift, re-run the deployment.py script
deployment.store_model_into_pickle()


# Diagnostics and reporting
# run diagnostics.py and reporting.py for the re-deployed models
diagnostics.model_predictions(None)
diagnostics.dataframe_summary(None)
diagnostics.execution_time()
diagnostics.outdated_packages_list()
diagnostics.missing_data(None)

# performing reporting
reporting.score_model()
