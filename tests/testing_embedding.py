from openai import OpenAI
def embed_chunks(client, chunks, model="text-embedding-3-small"):
    
    response = client.embeddings.create(
        model=model,
        input=chunks  # list of strings
    )
    embeddings = [record.embedding for record in response.data]

    return embeddings

if __name__ == "__main__":
    client = OpenAI()
    chunks = ["Hello, world!", "This is a test."]
    embeddings = embed_chunks(client, chunks)
    print(embeddings)
