import os
import csv
from uuid import uuid4
import numpy as np
import random
from pinecone import Pinecone, ServerlessSpec, Index
from sentence_transformers import SentenceTransformer
from helper_code.extract_510k import get_all_links, get_k_numbers
from helper_code.extract import download_pdf_to_file, extract_content_from_pdf
# from unstructured.partition.pdf import partition_pdf
# from unstructured.chunking.title import chunk_by_title
from dotenv import load_dotenv


def get_dataset_from_csv(csv_file_path):
    """
    Get a dataset of all the 510k documents and their corresponding links from a csv

    :param csv_file_path Filename where the metadata is stored
    :return: list of dictionaries about the documents
    """

    # Initialize an empty list to hold dictionaries
    data_list = []

    # Open the CSV file and read each row into a dictionary
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        # Use DictReader to directly create dictionaries from the CSV rows
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append(row)

    return data_list

def get_dataset(input_filename, number_docs = 20, specific_k_numbers=[]):
    """
    Get a dataset of all the 510k documents and their corresponding links

    :param input_filename Filename where the K numbers for the documents will be/is stored
    :param number_docs (optional): Number of 510k documents to process
    :return: list of dictionaries about the documents
    """
    if len(specific_k_numbers) > 0:
        pdfs = get_all_links(specific_k_numbers, number_docs)
        return pdfs
    
    k_numbers = get_k_numbers(input_filename)
    pdfs = get_all_links(k_numbers, number_docs)

    return pdfs

def encode_data(data, model):
    """
    Create an embedding using a specific model

    :param data: The text that needs to be encoded
    :param model: Model to create embedding
    :return: embedding in vector format
    """
    embeddings = model.encode(data)
    return embeddings

def get_index(index_name):
    """
    Get Pinecone index for a db by grabbing an existing or creating a new one

    :param index_name: Name of the desired index
    :return: Pinecone Index
    """
    load_dotenv()
    PINECONE_API = os.environ.get("PINECONE_API_KEY")
    pc = Pinecone(api_key=PINECONE_API)
    existing_indexes = pc.list_indexes()
    
    index_found = False
    for index in existing_indexes.indexes:
        if index.name == index_name: index_found = True
        

    # Check if a specific index exists
    if not index_found:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="euclidean",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-west-2'
            ) 
        ) 
    
    # get index
    index = pc.Index(index_name)
    return index
    
def get_sections(url, k_number):
    """
    Split the 510k document into sections

    :param url: Url of where the document is hosted
    :return: List of sections with id, title, and text.
    """
    filename = "./pdfs/" + k_number + ".pdf"
    print(filename)
    if os.path.exists(filename):
        pdf_file = filename
    else:
        pdf_file = download_pdf_to_file(url, filename)
    
    if pdf_file:

        sections = extract_content_from_pdf(filename)

        return sections
        
def create_chunks_metadata_embeddings(documents, model):
    """
    Given a dataset, split text data into chunks, extract metadata, create embeddings for each chunk.

    :param dataset: Data we want to process.
    :param model: Model that will be used to encode the text
    :return: List of data objects to upsert into our Pinecone index.
    """
    data_objs = []
    for document in documents:
        sections = get_sections(document["summary_url"], document["k_number"])
        for idx, section in enumerate(sections):
            try:
                payload = {
                "metadata": {
                    "k_number": document["k_number"],
                    "product_code": document["product_code"] if document["product_code"] else "",
                    "nct_code": document["nct_code"] if document["nct_code"] else "",
                    "section_title": section["title"],
                    "text_content": section["text"],
                    "type": section["type"]
                    },
                "id": str(uuid4()),
                "values": encode_data(str(section["text"]), model)
                }
                data_objs.append(payload)
            except:
                continue

    return data_objs

def batch_upsert(data: list[dict], index: Index, namespace: str, batch_size = 100):
    """
    Upsert data objects to a Pinecone index in batches.

    :param data: Data objects we want to upsert.
    :param index: Index into which we want to upsert our data objects.
    :namespace: Namespace within our index into which we want to upsert our data objects.
    """
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        index.upsert(vectors=batch, namespace=namespace)

def create_db(input_filename, number_docs, index_name, model_instance, namespace_name, specific_k_numbers=[], start=0, end=0):
    """
    Create Pinecone Vector DB

    :param input_filename Filename where the K numbers for the documents will be/is stored
    :param number_docs (optional): Number of 510k documents to process
    :param index_name: Name of the desired index
    :param model_instance: Model to create embedding
    :namespace: Namespace within our index into which we want to upsert our data objects.
    """
    print("GET DATA")
    # documents = get_dataset(input_filename, number_docs, specific_k_numbers)
    # LOAD IN CSV
    documents = get_dataset_from_csv('data/pdf_dataset.csv')

    print("CREATE INDEX")
    index = get_index(index_name)

    for i in range(start, end, 10):
        print("STARTING INDEX", i)

        specific_docs = documents[i: i+10]
        print("CREATE CHUNKS")
        data = create_chunks_metadata_embeddings(specific_docs, model_instance)

        print("UPSERT")
        batch_upsert(data, index, namespace_name)

        print("FINISHED INDEX", i+10)
    
if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')
    create_db(input_filename="./data/k_numbers.csv", number_docs=5, index_name="final-db-510k", model_instance=model, namespace_name="ns1", specific_k_numbers=[], start=0, end=1)