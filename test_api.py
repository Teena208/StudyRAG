from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Cybersecurity protects computer systems and data."
)

print("API connection successful!")
print("Embedding length:", len(response.data[0].embedding))