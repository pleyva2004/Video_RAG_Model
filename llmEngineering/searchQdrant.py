import os
import openai
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder
from qdrant_client import QdrantClient
from enhanceQuery import enhanceQuery 
from dummyEmbed import dummyEmbed

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)

# Initialize Cross-Encoder model
cross_encoder_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Retrieve candidates from Qdrant for one query embedding
def retrieveCandidates(query_embedding, collection_name="your_collection", top_k=10):
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    return search_results

# Cross-encoder reranking with the primary query only
def rerankWithCrossEncoder(primary_query_text, candidates):
    input_pairs = [(primary_query_text, candidate.payload['text']) for candidate in candidates]
    scores = cross_encoder_model.predict(input_pairs)
    reranked = [
        {
            'object_id': candidate.id,
            'score': score,
            'payload': candidate.payload
        }
        for candidate, score in zip(candidates, scores)
    ]
    reranked_sorted = sorted(reranked, key=lambda x: x['score'], reverse=True)
    return reranked_sorted

# Main function: broad retrieval, rerank with first enhanced query
def enhanceSearchAndRerank(raw_user_query, collection_name="your_collection", top_k=10, threshold=0.7):
    # Step 1: Enhance the query
    enhanced_queries = enhanceQuery(raw_user_query)
    print('enhanced queries')
    print(enhanced_queries)
    primary_query_text = enhanced_queries[0]  # Use the first enhanced query for reranking
    print()
    print('primary query')
    print(primary_query_text)

    # Step 2: Embed all enhanced queries
    query_embeddings = [dummyEmbed(query) for query in enhanced_queries]
    print("fix dummyEmbed")
    return

    # Step 3: Broad retrieval — gather candidates from all enhanced queries
    all_candidates = []
    seen_ids = set()  # To avoid duplicate candidates by ID

    for embedding in query_embeddings:
        candidates = retrieveCandidates(embedding, collection_name, top_k)
        for candidate in candidates:
            if candidate.id not in seen_ids:
                all_candidates.append(candidate)
                seen_ids.add(candidate.id)

    # Step 4: Rerank using cross-encoder with primary query only
    reranked_results = rerankWithCrossEncoder(primary_query_text, all_candidates)

    # Step 5: Filter by threshold
    filtered_results = [res for res in reranked_results if res['score'] >= threshold]

    return filtered_results
