from find_predicates import *
from pinecone import Pinecone
import numpy as np
from nomic import atlas
import nomic
import os 
from dotenv import load_dotenv

load_dotenv()
nomic.login(os.getenv("NOMIC_API_KEY"))

PINECONE_API = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API) 
index_name = "final-db-510k"
text_field = "text"

openai_api_key = os.environ.get('OPEN_AI_KEY') 
model_name = 'text-embedding-ada-002'
index = pc.Index(index_name) 

def get_pinecone_ids(user_data):
    embedding = embed_new_device(user_data)
    results = index.query(
        namespace="ns1",
        vector=embedding[0].tolist(),
        top_k=100,
        include_metadata=True, 
        filter={
            "section_title": "Device Description"
        },
    )

    print(results)

    all_vector_ids = {}
    if 'matches' in results:
        for match in results['matches']:
            try:
                id = match["id"]
                k_number = match["metadata"]["k_number"]
                all_vector_ids[id] = k_number
            except:
                continue
    
    return all_vector_ids 

def visualize(user_data):
    all_vector_ids= get_pinecone_ids(user_data)
    vectors = index.fetch(
        ids=list(all_vector_ids.keys()), 
        namespace="ns1"
    )

    print(vectors)

    ids = []
    embedding_vectors = []
    for id, vector in vectors['vectors'].items():
        ids.append(id)
        embedding_vectors.append(vector['values'])

    atlas.map_data(embeddings=np.array(embedding_vectors), data=[{'id': id, "k_number": k_num} for id, k_num in ids], id_field='id')

if __name__ == "__main__":
    device_description = "The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app."
    indications_for_use = "The Fitbit ECG App is a software-only mobile medical application intended for use with Fitbit wrist-wearable devices to create, record, store, transfer, and display a single channel electrocardiogram (ECG) qualitatively similar to a Lead I ECG. The Fitbit ECG App determines the presence of atrial fibrillation (AFib) or sinus rhythm on a classifiable waveform. The AF detection function is not recommended for users with other known arrhythmias. The Fitbit ECG App is intended for over-the-counter (OTC) use. The ECG data displayed by the Fitbit ECG App is intended for informational use only. The user is not intended to interpret or take clinical action based on the device output without consultation of a qualified healthcare professional. The ECG waveform is meant to supplement rhythm classification for the purposes of discriminating AFib from normal sinus rhythm and not intended to replace traditional methods of diagnosis or treatment. The Fitbit ECG App is not intended for use by people under 22 years old."
    
    user_data = {
        "Device Description": device_description,
        "Indications for use": indications_for_use,
    }

    visualize(user_data)




