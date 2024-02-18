import pandas as pd
from io import StringIO
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from .chatgpt import ask_gpt
import re
import csv
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests

model = SentenceTransformer('all-MiniLM-L6-v2')
PINECONE_API = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API) 
index_name = "final-db-510k"
index = pc.Index(index_name) 

def fetch_trial_complete_information(nct_code):
    """
    Obtain the complete trial information

    Args:
        nct_code (str): NCT code of a trial

    Returns:
        _type_: _description_
    """    
    # Send a GET request to the URL
    url = f'https://clinicaltrials.gov/api/v2/studies/{nct_code}'
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Parse the response content as JSON 
            data = response.json() 
            protocol = data['protocolSection']
            description = protocol["descriptionModule"]["briefSummary"]
            eligibility = protocol['eligibilityModule']
            design = protocol['designModule'] 
            intervention = protocol["armsInterventionsModule"] # experimental and control 
            outcomes= protocol['outcomesModule']
            return {
                "nct_code":nct_code,
                "description":description,
                "eligibility":eligibility,
                "design": design,
                "intervention": intervention,
                "outcomes": outcomes,
            }
        except ValueError:
            # In case the response is not in JSON format
            return
            #return "The response could not be parsed as JSON."
    else:
        print("COULD NOT RETRIEVE INFORMATION ABOUT THE TRIAL!")
        return
        # If the request was unsuccessful
        #return f"Request failed with status code: {response.status_code}"

def similar_clinical_trials(device_description):  
    """
    Given the device_description, get the similar trials

    Args:
        device_description (str): brief summary of the goal

    Returns:
        list: dictionaries of top 3 nct ids and summaries of clinical trials
    """  
    summary_embedding = model.encode(device_description)
    
    results = index.query(
        namespace="ns2",
        vector=summary_embedding.tolist(),
        top_k=7,
        include_metadata=True
    )
    
    clinical_trials = []
    for result in results['matches']:
        # iterate through and check scores: 
        nct_code = result["metadata"]["nct_code"]
        description = result["metadata"]["description"] 
        score = result["score"] 
        
        clinical_trials.append({
            "nct_code": nct_code,
            "description": description,
            "score": score,
        })
    
    clinical_trials.sort(key=lambda x: x["score"], reverse=True)

    return clinical_trials[:3]

def get_single_trial_information(clinical_trial):  
    """
    Get the clinical trial information (study design, outcomes, and more)

    Args:
        clinical_trial (dict): clinical trial information

    Returns:
        list: clinical trial with the updated information
    """  
    nct_code = clinical_trial["nct_code"]
    information = fetch_trial_complete_information(nct_code)
    trial_info = [["Category", "Clinical Trial Specific Information"]]
    for key in ["nct_code", "description", "eligibility", "design", "intervention", "outcomes"]:
        trial_info.append([key, information[key]])
    return trial_info

def get_multiple_trials_information(clinical_trials):  
    """
    Get the clinical trial information (study design, outcomes, and more)

    Args:
        clinical_trials (list): each element is a dictionary with clinical trial information

    Returns:
        list: clinical trials with the updated information
    """    
    all_trials = []
    for i in range(len(clinical_trials)):
        trial = clinical_trials[i]
        trial_info = get_single_trial_information(trial)
        all_trials.append(trial_info)
    
    return all_trials

def get_all_similar_trials(device_description):
    clinical_trials = similar_clinical_trials(device_description)
    print("SIMILAR CLINICAL TRIAL", clinical_trials)
    all_trials = get_multiple_trials_information(clinical_trials)
    return all_trials

if __name__ == "__main__":
    # nct_code = 'NCT05668377'
    # single_trial = fetch_trial_complete_information(nct_code)
    # print("SINGLE TRIAL", single_trial)

    device_description = "The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app."
    all_trials = get_all_similar_trials(device_description)
    print("ALL TRIALS INFORMATION", all_trials)