import os
import csv
import requests
from uuid import uuid4
from create_vector_db import batch_upsert, encode_data, get_index
import numpy as np
import random
from pinecone import Pinecone, ServerlessSpec, Index
from sentence_transformers import SentenceTransformer
from helper_code.extract_510k import get_all_links, get_k_numbers
from helper_code.extract import download_pdf_to_file, extract_content_from_pdf
# from unstructured.partition.pdf import partition_pdf
# from unstructured.chunking.title import chunk_by_title
from dotenv import load_dotenv

def fetch_trial_description(rank):
    # Send a GET request to the URL
    url = f'https://classic.clinicaltrials.gov/api/query/full_studies?expr=AREA[IsUnapprovedDevice]Yes OR AREA[IsFDARegulatedDevice]Yes&min_rnk={rank}&max_rnk={rank+1}&fmt=json'
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Parse the response content as JSON 
            data = response.json() 
            protocol = data['FullStudiesResponse']['FullStudies'][0]['Study']["ProtocolSection"]
            description = protocol["DescriptionModule"]["BriefSummary"]
            nct_code = protocol["IdentificationModule"]["NCTId"]

            return {
                "nct_code":nct_code,
                "description":description,
            }
        except ValueError:
            # In case the response is not in JSON format
            return
            #return "The response could not be parsed as JSON."
    else:
        print("STATUS CODE NOT GOOD!!")
        return
        # If the request was unsuccessful
        #return f"Request failed with status code: {response.status_code}"

def create_embeddings(record, model):
    """
    Given a record, create embeddings for the descriptions.

    :param record: Data we want to process.
    :param model: Model that will be used to encode the text
    :return: List of data objects to upsert into our Pinecone index.
    """
    payload = {
        "metadata": record,
        "id": str(uuid4()),
        "values": encode_data(str(record["description"]), model)
    }

    return payload

def create_clinical_trials_vector_db(index_name, model_instance, namespace_name, start, end):
    ## GET DATASET

    print("CREATE INDEX")
    index = get_index(index_name)

    data_to_upsert = []
    rank = start
    while rank < end:

        print("STARTING INDEX", rank)

        trial_info = fetch_trial_description(rank)

        if trial_info is not None and "nct_code" in trial_info and "description" in trial_info:
            data_to_upsert.append(create_embeddings(trial_info, model_instance))
        
        print("FINISHED INDEX", rank)

        if rank % 10 == 0:
            print("UPSERT PREVIOUS DATA")
            batch_upsert(data_to_upsert, index, namespace_name)
            data_to_upsert = []
        
        rank += 1
    
    batch_upsert(data_to_upsert, index, namespace_name)
    
    return 
    
if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')
    create_clinical_trials_vector_db(index_name="final-db-510k", model_instance=model, namespace_name="ns2", start=2, end=6000)