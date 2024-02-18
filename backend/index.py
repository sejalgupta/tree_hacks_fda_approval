from dotenv import load_dotenv
load_dotenv()
from helper_code.finetune_clinicals import generate_eligibility
from helper_code.generate_my_trial import generate_my_clinical_trial
from helper_code.find_similar_clinical_trial import get_all_similar_trials
from helper_code.visualization import visualize
from helper_code.find_predicates import get_final_comparison_table, parallel_process, predicates
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
import nomic
import os

app = Flask(__name__)
CORS(app) #, resources={r"/api/*": {"origins": "https://tree-hacks-fda-approval-n8ognjakq-treehacks.vercel.app", "allow_headers": "*", "allow_methods": "*"}})
# CORS(app, resources={r"/api/*": {"origins": "https://tree-hacks-fda-approval-n8ognjakq-treehacks.vercel.app"}})

nomic.login(os.getenv("NOMIC_API_KEY"))

@app.route("/api/home")
@cross_origin()
def home():
    return "Hello, hello!"

@app.route("/api/python")
@cross_origin()
def go_to_dashboard():
    return redirect('/dashboard')

@app.route("/api/handle-form", methods=['POST'])
@cross_origin()
def handle_form():
    # Retrieve form data
    device_description = request.form['device-description']
    indication_for_use = request.form['use-indication']
    k_number_description = request.form.get('k-number-description', None) #{
    k_number_use = request.form.get('k-number-use', None) #{
    k_number = request.form.get('k-number', None) #{
         #   "K": k_number,
          #  "Device Description": device_description,
           # "Indication for Use": indication_for_use,
        # }
    
    # Process the form data (for demonstration, print it to console)
    print(f"Device Description: {device_description}")
    print(f"Indication for Use: {indication_for_use}")

    device_data = {
        "Device Description": device_description,
        "Indication for Use": indication_for_use
    }
    all_information = []
    if not k_number:
        all_information = predicates(device_data)
        # if len(all_information) > 1:
        k_number_information = all_information[:1]
    else:
        k_number_information = [{
            "K": k_number,
            "Device Description": k_number_description,
            "Indication for Use": k_number_use
        }]
    print("---------------- K number information: \n\n\n", str(k_number_information))
    
    list_comparisons = parallel_process(k_number_information, device_description, indication_for_use)
    
    return {
        "k_number_information": all_information,
        "comparison_table": list_comparisons
    }

@app.route("/api/visualize-predicate", methods=['POST'])
@cross_origin()
def get_visualization_predicate():
    device_description = request.form['device-description']
    indication_for_use = request.form['use-indication']
    user_data = {
        "Device Description": device_description,
        "Indication for Use": indication_for_use
    }

    url = visualize(user_data, "ns1", "k_number", "Visualize the closest devices to your device")

    return {
        "url": url
    }

@app.route("/api/visualize-trials", methods=['POST'])
@cross_origin()
def get_visualization_trials():
    device_description = request.form['device-description']
    indication_for_use = request.form['use-indication']
    user_data = {
        "Device Description": device_description,
        "Indication for Use": indication_for_use
    }

    url = visualize(user_data, "ns2", "nct_code", "Visualize the closest clinical trials to your expected trial")

    return {
        "url": url
    }

@app.route("/api/similar-trials", methods=['POST'])
@cross_origin()
def similar_trials():
    device_description = request.form['device-description']
    all_trials = get_all_similar_trials(device_description)

    return {
        "all-trials": all_trials
    }

@app.route("/api/generate-trial", methods=['POST'])
@cross_origin()
def generate_trial():
    device_description = request.form['device-description']
    indications_use = request.form['use-indication']
    all_trials = request.form['all-trials']
    eligibility = generate_eligibility(device_description)
    trial_info = generate_my_clinical_trial(all_trials, device_description, indications_use, eligibility)

    return {
        "trial-info": trial_info
    }
