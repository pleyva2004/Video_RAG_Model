from featurizationPipeline.embedding import embed_chunks
from qdrant_client import QdrantClient

from openai import OpenAI
from dotenv import load_dotenv
import os

from sentence_transformers import CrossEncoder

from llmEngineering.enhance import enhanceQuery, newQuery
from llmEngineering.search import getRelevantChunks



def getResponse(query):
    load_dotenv()
    print("Starting...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant = QdrantClient(
        url="https://97972684-9c62-4969-8ddf-50078fdacceb.europe-west3-0.gcp.cloud.qdrant.io:6333", 
        api_key=os.getenv("QDRANT_API_KEY") 
    )
    groq = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),  # or replace with your key as a string
        base_url="https://api.groq.com/openai/v1"  # Groq's API endpoint
    )

    # Initialize Cross-Encoder model
    cross_encoder_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


    enhanced_queries = enhanceQuery(groq, query)
    # enhanced_queries = newQuery(groq, query)

    primary_query_text = enhanced_queries
    print(primary_query_text)

    embeddings = embed_chunks(client, primary_query_text)

    relevant_chunks = getRelevantChunks(qdrant, cross_encoder_model, primary_query_text, embeddings, collection_name="contextual_chunks", top_k=1)

    # for chunk in relevant_chunks:
    #     print()
    #     print(chunk.payload.get("timestamp"))
    #     print(chunk.payload.get("chunk_text"))

    # formatted_response = f"Excerpt: {relevant_chunks[0].payload.get('chunk_text')}\n\nRelevant Video Segment: {relevant_chunks[0].payload.get('timestamp')}"

    return relevant_chunks[0].payload
    


def enhanceResponse(chunk, query):


    groq = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),  # or replace with your key as a string
        base_url="https://api.groq.com/openai/v1"  # Groq's API endpoint
    )

    response = groq.chat.completions.create(
        model="llama3-8b-8192",  # Updated to current model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains topics based on provided context. Keep your explanations clear and concise."},
            {"role": "user", "content": f"Based on this context, explain the topic being discussed: {chunk} and the user's query: {query}"}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print(getResponse("explain the the binary cross entropy loss function"))