from helper_code.find_predicates import get_final_comparison_table, parallel_process, predicates
from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/api/handle-form", methods=['POST'])
def handle_form():
    # Retrieve form data
    device_description = request.form['device-description']
    indication_for_use = request.form['use-indication']
    
    # Process the form data (for demonstration, print it to console)
    print(f"Device Description: {device_description}")
    print(f"Indication for Use: {indication_for_use}")
    
    device_data = {
        "Device Description": device_description,
        "Indication for Use": indication_for_use
    }
    
    top_k_numbers = predicates(device_data)
    if len(k_number_information) > 3:
        k_number_information = k_number_information[:3]
    
    k_nums = []
    for info in k_number_information:
        k_nums.append(info["K"])

    list_comparisons = parallel_process(k_number_information, device_description, indication_for_use)
    
    return {
        "k_numbers": [top_k_numbers[0]],
        "comparison_table": list_comparisons
    }