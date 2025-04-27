from featurizationPipeline.embedding import embed_chunks
from qdrant_client import QdrantClient

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


    enhanced_queries = enhanceQuery(groq, query)

    primary_query_text = enhanced_queries[0]

    embeddings = embed_chunks(client, enhanced_queries)

    relevant_chunks = getRelevantChunks(qdrant, cross_encoder_model, primary_query_text, embeddings, collection_name="contextual_chunks", top_k=1)

    # for chunk in relevant_chunks:
    #     print()
    #     print(chunk.payload.get("timestamp"))
    #     print(chunk.payload.get("chunk_text"))

    formatted_response = f"Excerpt: {relevant_chunks[0].payload.get('chunk_text')}\n\nRelevant Video Segment: {relevant_chunks[0].payload.get('timestamp')}"

    return formatted_response
    


