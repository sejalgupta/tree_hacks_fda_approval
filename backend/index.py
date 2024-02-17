from helper_code.find_predicates import get_final_comparison_table, predicates
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

    list_comparisons = []

    for k_number in top_k_numbers:
        comparison_table = get_final_comparison_table(k_number, "Comparison with Predicate Device", device_description, indication_for_use)
        list_comparisons.append(comparison_table)

    return {
        "k_numbers": top_k_numbers,
        "comparison_table": list_comparisons
    }