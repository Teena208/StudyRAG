from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Cybersecurity protects computer systems and data."

embedding = model.encode(text)

print("Local embedding successful!")
print("Embedding length:", len(embedding))