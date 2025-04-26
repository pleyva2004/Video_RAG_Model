
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

def upload_embeddings(client, embeddings, chunks, timestamps, collection_name="contextual_chunks"):

    # Create a collection for the leather features
    vector_size = embeddings[0].shape[0]  # Get dimension from first feature vector

    # Create the collection
    client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

    # Insert the features into Qdrant
    points = []
    for idx, embedding in enumerate(embeddings):
        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "chunk_id": idx,
                    "chunk_text": chunks[idx],
                    "chunk_start_time": timestamps[idx][0],
                    "chunk_end_time": timestamps[idx][1]
                },
            )
        )


    # Upload in batches
    client.upsert(collection_name=collection_name, points=points)

    return len(points), collection_name