import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to our existing ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Open our collection
collection = client.get_collection(name="study_material")

# Ask a question
question = "What is phishing?"

# Convert the question into an embedding
question_embedding = model.encode(question).tolist()

# Search ChromaDB
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

# Show the results
print("\nMost relevant chunks:\n")

for i in range(len(results["documents"][0])):
    print(f"--- Result {i + 1} ---")
    print(f"Slide: {results['metadatas'][0][i]['slide']}")
    print(results["documents"][0][i])
    print()