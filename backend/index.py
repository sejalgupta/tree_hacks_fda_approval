from dotenv import load_dotenv
load_dotenv()
from helper_code.finetune_clinicals import generate_eligibility
from helper_code.generate_my_trial import generate_my_clinical_trial
from helper_code.find_similar_clinical_trial import get_all_similar_trials
from helper_code.visualization import visualize
from helper_code.find_predicates import get_final_comparison_table, parallel_process, predicates
from flask import Flask, render_template_string, request, redirect, url_for
from flask_cors import CORS, cross_origin
import nomic
import os

app = Flask(__name__)
CORS(app)

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
    
    return {
        "k_number_information": [{
            "K": "K123456",
            "Device Description": "Device 1",
            "Indication for Use": "Use 1"
        }],
        "comparison_table": [
            [
                ["", "Header 1", "Header 2"],
                ["Row 1", "In the heart of the forest, a stream whispers its secrets to the wind, while sunlight filters through the leaves, painting patterns on the forest floor in dappled shades of green.", "The old oak tree stood tall, its branches reaching out like arms embracing the sky."],
                ["Row 2", "Lost in the labyrinth of city streets, strangers pass like ships in the night, each with a story untold, each with a destination yet to be discovered.", "Amidst the chaos of the bustling marketplace, a street performer captivates the crowd with his mesmerizing melodies, transporting them to a world of magic and wonder."],
                ["Row 3", "Beneath the starlit sky, waves crash against the rugged cliffs, their thunderous applause echoing through the silent night.", "The salty breeze carries whispers of tales from distant lands, mingling with the sounds of seagulls crying out over the restless sea."],
                ["Row 4", "Through the window, the first light of dawn paints the room in hues of gold and pink, awakening the world to a new day.", "In the cozy warmth of the kitchen, the aroma of freshly baked bread fills the air, evoking memories of simpler times."],
                ["Row 5", "Nestled in the embrace of rolling hills, a quaint village sleeps soundly under the stars, its secrets hidden within the whispers of the night.", "A solitary figure stands atop the mountain, gazing out over the vast expanse below, finding solace in the quiet majesty of nature."]
            ]
        ]
    }

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