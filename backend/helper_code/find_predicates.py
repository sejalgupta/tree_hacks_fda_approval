import json
import pandas as pd
from io import StringIO
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from chatgpt import ask_gpt
import re
import csv
from sentence_transformers import SentenceTransformer

def retrieve_pinecone(k_number, section_title):
    load_dotenv()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode("")

    PINECONE_API = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=PINECONE_API) 
    index_name = "final-db-510k"
    index = pc.Index(index_name) 

    results = index.query(
        vector=embedding.tolist(),
        filter={
            "section_title": section_title,
            "k_number": k_number
        },
        top_k=1,
        include_metadata=True
    )
    print(results)

    # get the table info 
    if len(results['matches']) > 0:
        result = results['matches'][0]["metadata"]["text_content"]
        return result
    return "" 

def embed_new_device(data):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        descript = model.encode(data["Device Description"])
        indication = model.encode(data["Indication for Use"]) 
        #for section in data: 
            #new_data= new_data + " " + section + ": " + data[section] # concatenate  
        return [descript,indication] 

def calculate_product_scores_general(data_list):
    # Find intersecting keys across all dictionaries
    intersecting_keys = set(data_list[0].keys())
    for data in data_list[1:]:
        intersecting_keys &= set(data.keys())

    # Calculate the product of scores for intersecting keys
    product_scores = {}
    for key in intersecting_keys:
        product_score = 1
        for data in data_list:
            product_score *= data[key]
        product_scores[key] = product_score

    # Sort the keys by their product score in ascending order
    sorted_keys = sorted(product_scores, key=product_scores.get)

    final_list = [(key, product_scores[key]) for key in sorted_keys]
    results = [] 
    for x in final_list:
        results.append(x[0]) 
    return results

def predicates(user_data):  
    """
    Given the device description and intended use, get the similar devices

    Args:
        user_data (dict): two keys with Device Description and Indication for Use

    Returns:
        list: top 3 k numbers of devices that are similar
    """  

    PINECONE_API = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=PINECONE_API) 
    index_name = "final-db-510k"
        #index = pc.Index(index_name)
        #index.describe_index_stats()
    index = pc.Index(index_name) 
    description_embedding = embed_new_device(user_data)
    descript_embedding = description_embedding[0] 
    indicat_embedding = description_embedding[1]
  
    results_devices = index.query(
        namespace="ns1",
        vector=descript_embedding.tolist(),
        filter={
            "section_title": "Device Description"
        },
        top_k=7,
        include_metadata=True
    )

    results_intended_use = index.query(
        namespace="ns1",
        vector=indicat_embedding.tolist(),
        filter={
            "section_title": "Indications for use"
        },
        top_k=7,
        include_metadata=True
    )  
    
    # get top 3 k numbers 
# create a matrix of [7x7] and scores 
    
    top_3_predicates_devices = {}
    top_3_predicates_uses = {} 
    for result in results_devices['matches']:
        # iterate through and check scores: 
        knumber = result["metadata"]["k_number"] 
        score = result["score"] 
        if knumber not in top_3_predicates_devices: 
            # say it's decently confident and print score 
            top_3_predicates_devices[knumber] = score
    for result in results_intended_use['matches']:
        # iterate through and check scores: 
        knumber = result["metadata"]["k_number"] 
        score = result["score"] 
        if knumber not in top_3_predicates_uses: 
            # say it's decently confident and print score 
            top_3_predicates_uses[knumber] = score

    # if not then it's denovo
    # take each of these predicates and create a similarity score 
    

    predicates_list = [top_3_predicates_devices,top_3_predicates_uses] 
    return calculate_product_scores_general(predicates_list) 

def get_vector_db_table_information(k_number, section_title):
    """
    Get the table text from the vector db for the predicate

    Args:
        k_number_information (dict): the predicate device's k number

    Returns:
        list of list: The table content in LOL format
    """    

    # GET THE TABLE EXTRACTION TO WORK
    # k_number = k_number_info["k_number"]
    # table_info = retrieve_pinecone(k_number, section_title)
    # try:
    #     table = json.loads(table_info)
    #     return table
    # except:
    #     print("no table in db")

    table = [["Comparison Fields", "Predicate Device"]]
    for key in ["Device Description", "Indication for Use"]:
        try:
          table.append([key, k_number_info[key]])
        except:
            continue
        
    return table

def get_ground_truth_table(data):
    """
    Get the version of the comparison to predicate table without any content modifications

    Args:
        data (list): list of lists that contain information about the predicate device

    Returns:
        Pandas Dataframe: dataframe with columns for the Comparison Fields, Predicate Device, Subject Device, Comparison
    """    
    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    # Keep the first two columns
    df = df.iloc[:, :2]

    # Rename the columns
    rename_dict = {df.columns[0]: 'Comparison Fields', df.columns[1]: 'Predicate Device'}
    df.rename(columns=rename_dict, inplace=True)

    # Add in columns for the current device and the comparison
    df["Subject Device"] = "insert here"
    df["Comparison"] = "insert here"

    return df

def populate_fields_chatgpt(df, device_description, indications_use):
    output = StringIO()
    df.to_csv(output, index=False)  # Set index=False to exclude row indices in the output
    csv_string = output.getvalue()

    print("ORIGINAL", csv_string)

    prompt = f"""I have a table that compares a subject device to a predicate device on a number of conditions. 
    
    Here is the current version of the table: {csv_string}

    Currently, the table is missing information about the subject device and the comparison between the predicate and subject devices. 

    This is the known information about the subject device:
    1. Device Description: {device_description}
    2. Indications for Use: {indications_use}

    Can you please output only an updated version of the table with filling any missing fields in concise writing with the given information? The format of your output should be in this format {csv_string}
    """

    response = ask_gpt(prompt)
    print("GPT RESPONSE", response)

    answer_csv_string = response["choices"][0]["message"]["content"]
    print("CSV STRING", answer_csv_string)
    
    csv_buffer = StringIO(answer_csv_string)

    data = []
    csv_reader = csv.reader(csv_buffer)
    
    for row in csv_reader:
        if len(row) == 4:
            data.append(row)

    print("FINAL LIST OF LISTS", data)
    
    return data

def get_final_comparison_table(k_number_info, section_title, device_description, indications_for_use):
    """_summary_

    Args:
        k_number (_type_): _description_
        section_title (_type_): _description_
        device_description (_type_): _description_
        indications_for_use (_type_): _description_

    Returns:
        _type_: _description_
    """    
    table = get_vector_db_table_information(k_number_info, section_title)
    df = get_ground_truth_table(table)
    data = populate_fields_chatgpt(df, device_description, indications_for_use)

    return data

if __name__ == "__main__":
    
    device_description = "The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app."
    indications_for_use = "The Fitbit ECG App is a software-only mobile medical application intended for use with Fitbit wrist-wearable devices to create, record, store, transfer, and display a single channel electrocardiogram (ECG) qualitatively similar to a Lead I ECG. The Fitbit ECG App determines the presence of atrial fibrillation (AFib) or sinus rhythm on a classifiable waveform. The AF detection function is not recommended for users with other known arrhythmias. The Fitbit ECG App is intended for over-the-counter (OTC) use. The ECG data displayed by the Fitbit ECG App is intended for informational use only. The user is not intended to interpret or take clinical action based on the device output without consultation of a qualified healthcare professional. The ECG waveform is meant to supplement rhythm classification for the purposes of discriminating AFib from normal sinus rhythm and not intended to replace traditional methods of diagnosis or treatment. The Fitbit ECG App is not intended for use by people under 22 years old."
    
    user_data = {
        "Device Description": device_description,
        "Indication for Use": indications_for_use,
    }
    
    k_number_information = predicates(user_data)
    print(k_number_information)
    
    list_comparisons = []
    for k_number_info in k_number_information:
      comparison_table = get_final_comparison_table(k_number_info, "Comparison with Predicate Device", device_description, indications_for_use)
      list_comparisons.append(comparison_table)
    
    print(list_comparisons)
