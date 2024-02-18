import csv
from io import StringIO
from .chatgpt import ask_gpt
from .find_similar_clinical_trial import get_all_similar_trials


def generate_clinical_trial(all_trials, device_description, indications_use):
    csv_string = '''Category, Clinical Trial Specific Information
Description,use the device description without any commas
Eligibility,here is the eligibility without any commas
Design, here is the design without any commas
Intervention, here is the intervention without any commas
Outcomes, here is the outcomes without any commas'''

    prompt = f"""I want to create a table that creates a study design for a new device that I have created. 

    This is the known information about the subject device:
    1. Device Description: {device_description}
    2. Indications for use: {indications_use}

    Here are some clinical trials that have similar designs to mine: {all_trials}

    Can you please output a table with the complete information about the proposed clinical trial with 6 rows that have the titles "Category", "Description", "Eligibility", "Design", "Intervention", "Outcomes"? 
    
    The format of your output should only be in a CSV string format like this {csv_string}
    """
    
    response = ask_gpt(prompt)
    print("GPT RESPONSE", response)

    answer_csv_string = response["choices"][0]["message"]["content"]
    print("CSV STRING", answer_csv_string)
    
    csv_buffer = StringIO(answer_csv_string)

    data = []
    csv_reader = csv.reader(csv_buffer)
    
    for row in csv_reader:
        if len(row) == 2 and row[0] in ["Category", "Description", "Eligibility", "Design", "Intervention", "Outcomes"]:
            data.append(row)

    print("FINAL LIST OF LISTS", data)
    
    return data

if __name__ == "__main__":
    indications_for_use = "The Fitbit ECG App is a software-only mobile medical application intended for use with Fitbit wrist-wearable devices to create, record, store, transfer, and display a single channel electrocardiogram (ECG) qualitatively similar to a Lead I ECG. The Fitbit ECG App determines the presence of atrial fibrillation (AFib) or sinus rhythm on a classifiable waveform. The AF detection function is not recommended for users with other known arrhythmias. The Fitbit ECG App is intended for over-the-counter (OTC) use. The ECG data displayed by the Fitbit ECG App is intended for informational use only. The user is not intended to interpret or take clinical action based on the device output without consultation of a qualified healthcare professional. The ECG waveform is meant to supplement rhythm classification for the purposes of discriminating AFib from normal sinus rhythm and not intended to replace traditional methods of diagnosis or treatment. The Fitbit ECG App is not intended for use by people under 22 years old."
    device_description = "The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app."
    all_trials = get_all_similar_trials(device_description)
    generate_clinical_trial(all_trials, device_description, indications_for_use)