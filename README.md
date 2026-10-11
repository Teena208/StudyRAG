# StudyRAG — AI-Powered Study Assistant

StudyRAG is a local AI-powered study assistant that answers questions using information retrieved from study materials. It uses Retrieval-Augmented Generation (RAG) to provide answers with source slide references.

## Features

- Extracts text from PowerPoint study material.
- Generates semantic embeddings using Sentence Transformers.
- Stores and retrieves relevant content using ChromaDB.
- Generates answers using a locally running Llama model through Ollama.
- Provides a Streamlit web interface.
- Displays source slide numbers for retrieved content.

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- ChromaDB
- Ollama
- Llama 3.2 (1B)

## How It Works

1. Extract text from study material.
2. Convert text into vector embeddings.
3. Store embeddings in ChromaDB.
4. Convert a user's question into an embedding.
5. Retrieve relevant study content.
6. Send the retrieved context to the local Llama model.
7. Display the generated answer and source slides.

## Run Locally

1. Install Python and Ollama.
2. Download the model:

   `ollama pull llama3.2:1b`

3. Create and activate a virtual environment.
4. Install the required Python packages.
5. Run the application:

   `python -m streamlit run app.py`

## Project Status

The core RAG pipeline and Streamlit interface have been implemented and tested with PowerPoint study material. Further improvements to answer accuracy and document-upload support are planned.
