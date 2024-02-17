from helper_code.find_predicates import get_final_comparison_table, parallel_process, predicates
from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/api/handle-form", methods=['POST'])
def handle_form():
    # Retrieve form data
    device_description = request.form['device-description']
    indication_for_use = request.form['use-indication']
    k_number_information = request.form['k-number-information'] #{
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
    if not k_number_information:
        all_information = predicates(device_data)
        # if len(all_information) > 1:
        k_number_information = all_information[:1]

    list_comparisons = parallel_process(k_number_information, device_description, indication_for_use)
    
    return {
        "k_number_information": all_information,
        "comparison_table": list_comparisons
    }


    # return {
    #     "k_numbers": ["K123456", "K789012"],
    #     "comparison_table": [
    #         [
    #             ["", "Header 1", "Header 2"],
    #             ["Row 1", "In the heart of the forest, a stream whispers its secrets to the wind, while sunlight filters through the leaves, painting patterns on the forest floor in dappled shades of green.", "The old oak tree stood tall, its branches reaching out like arms embracing the sky."],
    #             ["Row 2", "Lost in the labyrinth of city streets, strangers pass like ships in the night, each with a story untold, each with a destination yet to be discovered.", "Amidst the chaos of the bustling marketplace, a street performer captivates the crowd with his mesmerizing melodies, transporting them to a world of magic and wonder."],
    #             ["Row 3", "Beneath the starlit sky, waves crash against the rugged cliffs, their thunderous applause echoing through the silent night.", "The salty breeze carries whispers of tales from distant lands, mingling with the sounds of seagulls crying out over the restless sea."],
    #             ["Row 4", "Through the window, the first light of dawn paints the room in hues of gold and pink, awakening the world to a new day.", "In the cozy warmth of the kitchen, the aroma of freshly baked bread fills the air, evoking memories of simpler times."],
    #             ["Row 5", "Nestled in the embrace of rolling hills, a quaint village sleeps soundly under the stars, its secrets hidden within the whispers of the night.", "A solitary figure stands atop the mountain, gazing out over the vast expanse below, finding solace in the quiet majesty of nature."]
    #         ],
    #         [
    #             ["", "Header 1", "Header 2"],
    #             ["Row 1", "In the heart of the forest, a stream whispers its secrets to the wind, while sunlight filters through the leaves, painting patterns on the forest floor in dappled shades of green.", "The old oak tree stood tall, its branches reaching out like arms embracing the sky."],
    #             ["Row 2", "Lost in the labyrinth of city streets, strangers pass like ships in the night, each with a story untold, each with a destination yet to be discovered.", "Amidst the chaos of the bustling marketplace, a street performer captivates the crowd with his mesmerizing melodies, transporting them to a world of magic and wonder."],
    #             ["Row 3", "Beneath the starlit sky, waves crash against the rugged cliffs, their thunderous applause echoing through the silent night.", "The salty breeze carries whispers of tales from distant lands, mingling with the sounds of seagulls crying out over the restless sea."],
    #             ["Row 4", "Through the window, the first light of dawn paints the room in hues of gold and pink, awakening the world to a new day.", "In the cozy warmth of the kitchen, the aroma of freshly baked bread fills the air, evoking memories of simpler times."],
    #             ["Row 5", "Nestled in the embrace of rolling hills, a quaint village sleeps soundly under the stars, its secrets hidden within the whispers of the night.", "A solitary figure stands atop the mountain, gazing out over the vast expanse below, finding solace in the quiet majesty of nature."]
    #         ]
    #     ]
    # }