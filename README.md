# Project: A Dynamic Risk Assessment System
This Repository holds the code for udacity project: A Dynamic Risk Assessment System

## Background
Imagine that you're the Chief Data Scientist at a big company that has 10,000 
corporate clients. Your company is extremely concerned about attrition risk: the
risk that some of their clients will exit their contracts and decrease the company's 
revenue. They have a team of client managers who stay in contact with clients and try 
to convince them not to exit their contracts. However, the client management team is 
small, and they're not able to stay in close contact with all 10,000 clients.

The company needs you to create, deploy, and monitor a risk assessment ML model 
that will estimate the attrition risk of each of the company's 10,000 clients. 
If the model you create and deploy is accurate, it will enable the client managers 
to contact the clients with the highest risk and avoid losing clients and revenue.

Creating and deploying the model isn't the end of your work, though. Your industry 
is dynamic and constantly changing, and a model that was created a year or a month 
ago might not still be accurate today. Because of this, you need to set up regular 
monitoring of your model to ensure that it remains accurate and up-to-date. You'll 
set up processes and scripts to re-train, re-deploy, monitor, and report on your ML 
model, so that your company can get risk assessments that are as accurate as possible 
and minimize client attrition.

## Project overview
You'll complete the project by proceeding through 5 steps:

* Data ingestion. Automatically check a database for new data that can be used for 
model training. Compile all training data to a training dataset and save it to persistent 
storage. Write metrics related to the completed data ingestion tasks to persistent storage.
* Training, scoring, and deploying. Write scripts that train an ML model that predicts
attrition risk, and score the model. Write the model and the scoring metrics to persistent 
storage.
* Diagnostics. Determine and save summary statistics related to a dataset. Time the 
performance of model training and scoring scripts. Check for dependency changes and 
package updates.
* Reporting. Automatically generate plots and documents that report on model metrics. 
Provide an API endpoint that can return model predictions and metrics.
* Process Automation. Create a script and cron job that automatically run all previous 
steps at regular intervals.

### Workspace
* `/practicedata/`. This is a directory that contains some data you can use for practice.
* `/sourcedata/`. This is a directory that contains data that you'll load to train your models.
* `/ingesteddata/`. This is a directory that will contain the compiled datasets after your
ingestion script.
* `/testdata/`. This directory contains data you can use for testing your models.
* `/models/`. This is a directory that will contain ML models that you create for production.
* `/practicemodels/`. This is a directory that will contain ML models that you create as 
practice.
* `/production_deployment/`. This is a directory that will contain your final, deployed 
models.

### Files
* `training.py`, a Python script meant to train an ML model
* `scoring.py`, a Python script meant to score an ML model
* `deployment.py`, a Python script meant to deploy a trained ML model
* `ingestion.py`, a Python script meant to ingest new data
* `diagnostics.py`, a Python script meant to measure model and data diagnostics
* `reporting.py`, a Python script meant to generate reports about model metrics
* `app.py`, a Python script meant to contain API endpoints
* `wsgi.py`, a Python script to help with API deployment
* `apicalls.py`, a Python script meant to call your API endpoints
* `fullprocess.py`, a script meant to determine whether a model needs to be re-deployed, 
and to call all other Python scripts when needed

### Using `config.json` correctly
This file contains five entries:

* `input_folder_path`, which specifies the location where your project will look for input data, to ingest, and to use in model training. If you change the value of input_folder_path, your project will use a different directory as its data source, and that could change the outcome of every step.
* `output_folder_path`, which specifies the location to store output files related to data ingestion. In the starter version of config.json, this is equal to /ingesteddata/, which is the directory where you'll save your ingested data later in this step.
* `test_data_path`, which specifies the location of the test dataset
* `output_model_path`, which specifies the location to store the trained models and scores.
* `prod_deployment_path`, which specifies the location to store the models in production.

When we're initially setting up the project, our config.json file will be set to read 
`practicedata` and write `practicemodels`. When we're ready to finish the project, you will
need to change the locations specified in config.json so that we're reading our actual, 
`sourcedata` and we're writing to our models directory.

### Writing the dataset
Now that you have a single pandas DataFrame containing all of your data, 
you need to write that dataset to storage in your workspace. You can save it to a
file called `finaldata.csv`. Save this file to the directory that's specified in the 
`output_folder_path` entry of your `config.json` configuration file. In your starter 
version of `config.json`, the `output_folder_path` entry is set to `/ingesteddata/`, so 
your dataset will be saved to `/ingesteddata/`.


### Saving a record of the ingestion
For later steps in the project, you'll need to have a record of which files 
you read to create your `finaldata.csv` dataset. You need to create a record of 
all of the files you read in this step, and save the record on your workspace as a 
Python list.

You can store this record in a file called `ingestedfiles.txt`. This file should 
contain a list of the filenames of every .csv you've read in your `ingestion.py` script. 
You can also save this file to the directory that's specified in the `output_folder_path` 
entry of your `config.json` configuration file.

### Model Training

Build a function that accomplishes model training for an attrition risk assessment 
ML model. Your model training function should accomplish the following:

* Read in `finaldata.csv` using the pandas module. The directory that you read from is 
specified in the `output_folder_path` of your `config.json` starter file.
* Use the scikit-learn module to train an ML model on your data. The `training.py`
starter file already contains a logistic regression model you should use for training.
* Write the trained model to your workspace, in a file called `trainedmodel.pkl`. 
The directory you'll save it in is specified in the `output_model_path entry` of your 
`config.json`.

### Model Scoring

You need to write a function that accomplishes model scoring. You can write this function in the starter file called scoring.py. To accomplish model scoring, you need to do the following:

* Read in test data from the directory specified in the `test_data_path` of your 
`config.json` file
* Read in your trained ML model from the directory specified in the `output_model_path` 
entry of your `config.json` file
* Calculate the F1 score of your trained model on your testing data
* Write the F1 score to a file in your workspace called `latestscore.txt`. You should 
save this file to the directory specified in the `output_model_path` entry of your 
`config.json` file.

### Model Deployment

Finally, you need to write a function that will deploy your model. You can write this 
function in the starter file called `deployment.py`.

Your model deployment function will not create new files; it will only copy 
existing files. It will copy your trained model (`trainedmodel.pkl`), your model score 
(`latestscore.txt`), and a record of your ingested data (`ingestedfiles.txt`). It will 
copy all three of these files from their original locations to a production deployment
directory. The location of the production deployment directory is specified in the 
`prod_deployment_path` entry of your `config.json`
