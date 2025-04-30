from qdrant_client import QdrantClient
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import os

from featurizationPipeline.upload import upload_embeddings
from featurizationPipeline.embedding import embed_chunks
from featurizationPipeline.chunking import quality_focused_chunking


def upload_to_qdrant():
    load_dotenv()

    qdrant = QdrantClient(
        url="https://97972684-9c62-4969-8ddf-50078fdacceb.europe-west3-0.gcp.cloud.qdrant.io:6333", 
        api_key=os.getenv("QDRANT_API_KEY") 
    )
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    print("Reading transcript...")
    # with open(f"./assets/transcripts/{file_name}.txt", "r") as f:
    #     text = f.read()
    file_name = ["9CGGh6ivg68", "eFgkZKhNUdM", "eQ6UE968Xe4", "FCQ-rih6cHY", "lb_5AdUpfuA", "rCVlIVKqqGE",  "TV-DjM8242s", "WXoOohWU28Y"]
    indices = [1, 2, 3, 4, 5, 6, 7, 8]

    # with open(f"./assets/timestamps/{file_name}.txt", "r") as f:
    #     timestamps = [line.split() for line in f.readlines()]

    print("Chunking...")
    chunks_to_embed = []
    timestamp_to_payload = []
    video_id_list = []
    for j in indices:
        i = j - 1
        file = file_name[i]

        # chunks, timestamps = quality_focused_chunking(client, text, timestamps, j)
        with open(f"./assets/chunks/chunks_{j}.txt", "r") as f:
            chunks = f.readlines()
            chunks_to_embed.extend(chunks)

        with open(f"./assets/chunk_timestamps/chunks_{j}_timestamped.txt", "r") as f:
            timestamps = f.readlines()
            timestamps = [line.split()[:3] for line in timestamps if len(line) > 1]
            timestamps = [[line[0], line[2]] for line in timestamps]
            timestamp_to_payload.extend(timestamps)

        for chunk in chunks:
            video_id_list.append(file)
    
    for i, chunk in enumerate(chunks_to_embed):
        print(chunk, video_id_list[i])


    print(len(chunks_to_embed))
    
    print("Embedding...")
    # embeddings = embed_chunks(client, chunks_to_embed)
    
    # Save embeddings to a text file
    # print("Saving embeddings to file...")
    # np.save('./assets/embeddings/embeddings.npy', embeddings)
    # print("Embeddings saved successfully!")

    print("Loading embeddings...")
    embeddings = np.load('./assets/embeddings/embeddings.npy')

    
    print("Uploading embeddings...")
    num_points, collection_name = upload_embeddings(qdrant, embeddings, chunks_to_embed, timestamp_to_payload, video_id_list, "contextual_chunks")


    print(
        f"Uploaded {num_points} feature vectors to Qdrant collection '{collection_name}'"
    )

    print(qdrant.get_collections())

