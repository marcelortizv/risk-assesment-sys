from flask import Flask, request
from diagnostics import model_predictions, dataframe_summary, missing_data, execution_time, outdated_packages_list
from scoring import score_model
import json
import os


# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json', 'r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 

prediction_model = None


# Prediction Endpoint
@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():        
    """
    call the prediction function you created in Step 3
    :return:
    """
    dataset_path = request.json.get('dataset_path')
    y_pred, _ = model_predictions(dataset_path)
    return str(y_pred)


# Scoring Endpoint
@app.route("/scoring", methods=['GET', 'OPTIONS'])
def scoring():
    """
    Check the score of the deployed models
    :return:
    """
    score = score_model()
    return str(score)


# Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def stats():        
    """
    check means, medians, and modes for each column
    :return:
    """
    summary = dataframe_summary()
    return summary


# Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnostics():
    et = execution_time()
    md = missing_data()
    op = outdated_packages_list()
    return str("execution_time:" + et + "\nmissing_data;" + md + "\noutdated_packages:" + op)


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
