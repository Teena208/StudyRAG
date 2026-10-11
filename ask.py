print("Step 1: Starting...", flush=True)

import chromadb
print("Step 2: ChromaDB loaded!", flush=True)

from sentence_transformers import SentenceTransformer
print("Step 3: Embedding library loaded!", flush=True)

import requests
print("Step 4: Requests loaded!", flush=True)

print("Step 5: Loading embedding model...", flush=True)
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Step 6: Model ready!", flush=True)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="study_material")

print("Step 7: Database connected!", flush=True)

question = input("Ask your study question: ")

question_embedding = model.encode(question).tolist()

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

context = ""

for i in range(len(results["documents"][0])):
    slide = results["metadatas"][0][i]["slide"]
    text = results["documents"][0][i]
    context += f"\nSlide {slide}:\n{text}\n"

print("Step 8: Sending question to local AI...", flush=True)

prompt = f"""
Answer using only the study material below.
Explain in simple words.
If the answer is unavailable, say so.

Study material:
{context}

Question: {question}
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

print("\nStudyRAG Answer:\n")
print(response.json()["response"])

print("\nSources:")
for metadata in results["metadatas"][0]:
    print("Slide", metadata["slide"])