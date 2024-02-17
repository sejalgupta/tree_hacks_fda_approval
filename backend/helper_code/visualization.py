from pinecone import Pinecone
import numpy as np
from nomic import atlas
import nomic
import os 

#nomic.login(os.getenv("NOMIC_API_KEY"))

PINECONE_API = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API) 
index_name = "doc-510k"
    #index = pc.Index(index_name)
    #index.describe_index_stats()
text_field = "text"
#spec = ServerlessSpec(cloud='aws', region='us-west-2')

openai_api_key = os.environ.get('OPEN_AI_KEY') 
print(openai_api_key)
model_name = 'text-embedding-ada-002'
#num_embeddings = 

index = pc.Index(index_name) 
# need all ids to 
# only fetch the ones near you: top 20 
vectors = index.fetch(ids=[str(i) for i in range(2)])

ids = []
embeddings = []
for id, vector in vectors['vectors'].items():
    ids.append(id)
    embeddings.append(vector['values'])

ids = ["1","2","3",'4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
embeddings = np.array(embeddings)
num_vectors = 20

# Generate random embedding vectors
embedding_vectors = [np.random.rand(384) for _ in range(num_vectors)]

# Convert the list of arrays to a NumPy array
embedding_vectors = np.array(embedding_vectors)
atlas.map_data(embeddings=embedding_vectors, data=[{'id': id} for id in ids], id_field='id')




