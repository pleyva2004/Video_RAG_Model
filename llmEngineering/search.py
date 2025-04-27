# Retrieve candidates from Qdrant for one query embedding
def retrieveCandidates(client, query_embedding, collection_name, top_k=5):
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    return search_results

# Cross-encoder reranking with the primary query only
def rerankWithCrossEncoder(model, primary_query_text, candidates):
    input_pairs = [(primary_query_text, candidate.payload['chunk_text']) for candidate in candidates]
    scores = model.predict(input_pairs)
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
def getRelevantChunks(client, model, primary_query_text, query_embeddings, collection_name, top_k=5, threshold=0.7):

    # Step 3: Broad retrieval — gather candidates from all enhanced queries
    all_candidates = []
    seen_ids = set()  # To avoid duplicate candidates by ID

    for embedding in query_embeddings:
        candidates = retrieveCandidates(client, embedding, collection_name, top_k)
        for candidate in candidates:
            if candidate.id not in seen_ids:
                all_candidates.append(candidate)
                seen_ids.add(candidate.id)

    # Step 4: Rerank using cross-encoder with primary query only
    # reranked_results = rerankWithCrossEncoder(model, primary_query_text, all_candidates)

    # Step 5: Filter by threshold
    # filtered_results = [res for res in reranked_results if res['score'] >= threshold]
    # filtered_results = all_candidates[:3]
    # filtered_results = reranked_results[:top_k]

    return all_candidates
