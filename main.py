from featurizationPipeline.chunking import quality_focused_chunking
from featurizationPipeline.embedding import embed_chunks
from featurizationPipeline.upload import upload_embeddings

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from openai import OpenAI
from dotenv import load_dotenv
import os





def main():
    load_dotenv()
    print("Starting...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant = QdrantClient(":memory:")  # Using in-memory storage

    print("Reading transcript...")
    with open("./assets/eFgkZKhNUdM.txt", "r") as f:
        text = f.read()

    print("Chunking...")
    # chunks, timestamps = quality_focused_chunking(client, text)
    with open("./assets/chunks_new.txt", "r") as f:
        chunks = f.readlines()

    with open("./assets/chunks.txt", "r") as f:
        timestamps = f.readlines()
        timestamps = [line.split()[:3] for line in timestamps]
        timestamps = [[line[0], line[2]] for line in timestamps]

    
    # with open("chunks.txt", "w") as f:
    #     for i in range(len(chunks)):
    #         f.write(f"{timestamps[i][0]} - {timestamps[i][1]} : {chunks[i]}\n")
  
    print("Embedding...")
    embeddings = embed_chunks(client, chunks)
    
    print("Uploading embeddings...")
    num_points, collection_name = upload_embeddings(qdrant, embeddings, chunks, timestamps, "contextual_chunks")

    print(
    f"Uploaded {num_points} feature vectors to Qdrant collection '{collection_name}'"
    )

    
if __name__ == "__main__":
    main()