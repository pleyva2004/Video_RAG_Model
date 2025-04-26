import numpy as np

def embed_chunks(client, chunks, model="text-embedding-3-small"):
    
    response = client.embeddings.create(
        model=model,
        input=chunks  # list of strings
    )
    embeddings = [record.embedding for record in response.data]
    return np.array(embeddings)  # Convert to NumPy array

