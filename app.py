import streamlit as st
import chromadb
import requests
from sentence_transformers import SentenceTransformer


# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="StudyRAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyRAG")
st.write("AI-powered study assistant")


# -----------------------------
# Load embedding model
# -----------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# -----------------------------
# Connect to ChromaDB
# -----------------------------

@st.cache_resource
def load_database():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="study_material")
    return collection


collection = load_database()


# -----------------------------
# Question input
# -----------------------------

question = st.text_input(
    "Ask a question about your study material:"
)


# -----------------------------
# RAG pipeline
# -----------------------------

if question:

    with st.spinner("Searching your study material..."):

        # Convert question into an embedding
        question_embedding = model.encode(question).tolist()

        # Search ChromaDB
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )

        # Build context from retrieved slides
        context = ""

        for i in range(len(results["documents"][0])):

            slide = results["metadatas"][0][i]["slide"]
            text = results["documents"][0][i]

            context += f"""
Slide {slide}:
{text}

"""


    # -----------------------------
    # Generate answer using Ollama
    # -----------------------------

    with st.spinner("Generating answer..."):

        prompt = f"""
You are StudyRAG, an AI study assistant.

Answer the user's question using the study material provided below.

Rules:
- Give a direct and clear answer.
- Use the retrieved study material as the main source.
- Explain the answer in simple words.
- Do not add unrelated information.
- Do not invent facts that are not supported by the study material.
- If the study material contains enough information to answer the question, answer it.
- Only say "I could not find this information in the study material." if the retrieved material genuinely does not contain enough information.

Study material:
{context}

User question:
{question}

Answer:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        # Check whether Ollama responded successfully
        if response.status_code == 200:

            answer = response.json()["response"]

        else:

            answer = (
                "Sorry, I could not connect to the local AI model. "
                "Please make sure Ollama is running."
            )


    # -----------------------------
    # Display answer
    # -----------------------------

    st.subheader("💡 Answer")
    st.write(answer)


    # -----------------------------
    # Display sources
    # -----------------------------

    st.subheader("📖 Sources")

    for metadata in results["metadatas"][0]:

        st.write(
            f"Slide {metadata['slide']}"
        )