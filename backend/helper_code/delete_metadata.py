from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API) 
index_name = "final-db-510k"
index = pc.Index(index_name) 

index.delete(
    namespace="ns2",
    filter={
        "nct_code": "NCT04380415",
    }
)