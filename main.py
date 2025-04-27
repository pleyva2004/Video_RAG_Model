from featurizationPipeline.chunking import quality_focused_chunking
from featurizationPipeline.embedding import embed_chunks
from featurizationPipeline.upload import upload_embeddings

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from openai import OpenAI
from dotenv import load_dotenv
import os

from sentence_transformers import CrossEncoder

from llmEngineering.enhance import enhanceQuery
from llmEngineering.search import getRelevantChunks



def getResponse(query):
    load_dotenv()
    print("Starting...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant = QdrantClient(":memory:")  # Using in-memory storage
    groq = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),  # or replace with your key as a string
        base_url="https://api.groq.com/openai/v1"  # Groq's API endpoint
    )

    # Initialize Cross-Encoder model
    cross_encoder_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

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

    # dummy_query = "What is a binary classifier?"

    enhanced_queries = enhanceQuery(groq, query)

    primary_query_text = enhanced_queries[0]

    embeddings = embed_chunks(client, enhanced_queries)

    relevant_chunks = getRelevantChunks(qdrant, cross_encoder_model, primary_query_text, embeddings, collection_name, top_k=1)

    # for chunk in relevant_chunks:
    #     print()
    #     print(chunk.payload.get("timestamp"))
    #     print(chunk.payload.get("chunk_text"))

    formatted_response = f"Excerpt: {relevant_chunks[0].payload.get('chunk_text')}\n\nRelevant Video Segment: {relevant_chunks[0].payload.get('timestamp')}"

    return formatted_response
    


