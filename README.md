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
  - Video segment playback with precise timestamp control

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
