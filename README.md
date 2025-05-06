# Video_RAG-Model
Final Project creating a Video RAG Model 

## Overview
The Video RAG (Retrieval-Augmented Generation) Model is an intelligent system designed to process and analyze educational video content. It enables users to ask questions about video content and receive relevant video segments along with detailed answers.

## Pipeline Architecture

### 1. Video Processing Pipeline
- **Chunking**: The system processes video transcripts into semantic chunks using quality-focused chunking
- **Timestamp Mapping**: Each chunk is mapped to its corresponding video timestamp
- **Embedding Generation**: Chunks are converted into vector embeddings using OpenAI's text-embedding-3-small model

### 2. Storage Layer
- **Vector Database**: Uses Qdrant for efficient vector storage and retrieval
- **Metadata Storage**: MongoDB stores additional metadata about videos and chunks

### 3. Query Processing
- **Query Enhancement**: User queries are enhanced using LLM to improve search accuracy
- **Cross-Encoder Reranking**: Uses a cross-encoder model for precise relevance scoring
- **Semantic Search**: Retrieves relevant video segments based on semantic similarity

### 4. User Interface
- **Gradio Interface**: Provides a user-friendly web interface for:
  - Question input
  - Answer display
  - Video Showed
  - Timestamped for relevant frames shown

## Key Features
- Semantic search across video content
- Precise timestamp-based video segment retrieval
- Enhanced query understanding
- Interactive video playback interface
- Scalable vector storage solution

## Technical Stack
- Python 3.12
- OpenAI API for embeddings and LLM
- Qdrant for vector storage
- MongoDB for metadata
- Gradio for web interface
- Docker for containerization

## Implementation Details

### 1. Data Pipeline

The **data pipeline** is responsible for collecting, cleaning, and storing transcript and timestamp data from the videos.

- **Data Source**:  
  We began by downloading videos and their corresponding `.en.vtt` subtitle files from a HuggingFace-hosted dataset. These files were placed into the local `data/rawData/` directory.  
  > **Note**: The videos were not pushed to GitHub due to file size limits, but they remain available locally.

- **Transcript Cleaning**:  
  We parsed the `.en.vtt` files to extract timestamped captions. To enhance transcript quality, we:
  - Removed filler words like *"um"* and *"uh"*
  - Eliminated duplicate and overlapping phrases

- **Transcript Generation**:  
  Cleaned captions were concatenated into a full transcript. We saved:
  - Timestamps → `assets/timestamps/`
  - Full transcripts → `assets/transcripts/`

- **Database Insertion**:  
  Each video's transcript and timestamps were uploaded to **MongoDB** for structured access.  
  The orchestration of this process is handled by the `upload_to_mongoDB()` function in `populateMongo.py`.


### 2. Featurization Pipeline

The **featurization pipeline** converts the cleaned transcripts into searchable, semantically meaningful embeddings.

- **Data Retrieval**:  
  For each video, we retrieved its transcript and timestamps from MongoDB.

- **Semantic Chunking**:  
  Transcripts were divided into semantically coherent chunks using an **LLM**. The model returned paragraph-like sections with clear topical boundaries.

- **Timestamp Alignment**:  
  Each chunk was aligned with its start and end time using the original timestamp data.

- **Caching Outputs**:  
  To avoid redundant LLM calls and recomputation:
  - Raw semantic chunks → `assets/chunks/`
  - Timestamp-aligned chunks → `assets/chunk_timestamps/`

- **Embedding Generation**:  
  We embedded each chunk using a selected embedding model (e.g., OpenAI or Cohere). Embeddings were cached in `assets/embeddings/` for reuse.

- **Vector Store Upload (Qdrant)**:  
  We stored each chunk in **Qdrant**, with:
  - **Vector**: Chunk embedding
  - **Payload**:
    - Raw chunk text
    - Start and end timestamps
    - Video ID

> To run both the data and featurization pipelines, execute the `start()` function in `ETL.py`.


### 3. Inference Pipeline

The **inference pipeline** handles query enhancement, retrieval, and user-facing interaction.

- **Query Enhancement**:  
  When a user submits a question, we enhance it by passing it through an LLM. The model converts the question into a more detailed declarative statement, incorporating implied context.

- **Query Embedding & Retrieval**:  
  The enhanced query is embedded using the same model used for video chunks. We then query **Qdrant** to retrieve the most semantically similar chunk.

- **Result Formatting**:  
  Since we could not splice video clips directly, we return:
  - The start and end timestamps of the matched chunk
  - A short summary of the chunk’s content

- **Execution**:  
  The inference pipeline can be run by calling the `getResponse()` function in `LLM.py`.

- **Gradio Application**:  
  Our user interface is built using **Gradio**. The app:
  - Takes a user query
  - Returns the matched video ID, timestamps, and summary  
  > Run the app using `app.py`

  **Important**: The application requires access to a Qdrant API key, which we could not include in the repository due to GitHub's security policies.

- **Demonstration**:  
  To validate our system, we saved the output in `app.ipynb` and recorded a demonstration video.  
  📺 [**Watch our demo here**](<insert YouTube URL>)
