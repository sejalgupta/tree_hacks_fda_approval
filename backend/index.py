from backend.helper_code.find_similar_clinical_trial import get_all_similar_trials
from helper_code.find_predicates import get_final_comparison_table, parallel_process, predicates
from flask import Flask, render_template_string, request, redirect, url_for
app = Flask(__name__)

@app.route("/api/python")
def go_to_dashboard():
    return redirect('/dashboard')

@app.route("/api/handle-form", methods=['POST'])
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

@app.route("/api/similar-trials", methods=['POST'])
def similar_trials():
    device_description = request.form['device-description']
    all_trials = get_all_similar_trials(device_description)

    return {
        "all_trials": all_trials
    }