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
    with open("./dataPipeline/data/transcripts/eFgkZKhNUdM.txt", "r") as f:
        text = f.read()

    print("Chunking...")
    chunks = quality_focused_chunking(client, text)
  
    print("Embedding...")
    embeddings = embed_chunks(client, chunks)
    
    print("Uploading embeddings...")
    num_points, collection_name = upload_embeddings(qdrant, embeddings, "contextual_chunks")

    print(
    f"Uploaded {num_points} feature vectors to Qdrant collection '{collection_name}'"
    )

    
if __name__ == "__main__":
    main()