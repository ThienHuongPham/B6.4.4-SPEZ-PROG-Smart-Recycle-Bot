from openai import OpenAI
import requests, json, time
import pandas as pd
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AZURE_OPENAI_API_ENDPOINT = os.environ.get("AZURE_OPENAI_API_ENDPOINT")
DEPLOYMENT_NAME = "text-embedding-3-small-htw-test"

QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
COLLECTION = "abfall_docs"

client = OpenAI(
    base_url=f"{AZURE_OPENAI_API_ENDPOINT}",
    api_key=OPENAI_API_KEY
)

# Wait for Qdrant to be ready
while True:
    try:
        r = requests.get(f"{QDRANT_URL}/collections")
        if r.status_code == 200:
            break
    except:
        pass
    print("Waiting for Qdrant...")
    time.sleep(2)

# Delete existing collection if any
requests.delete(f"{QDRANT_URL}/collections/{COLLECTION}")

# Ensure collection exists
body = {"vectors": {"size": 1536, "distance": "Cosine"}}
requests.put(f"{QDRANT_URL}/collections/{COLLECTION}", json=body)

# Embed each row’s text
def embed(text):
    return client.embeddings.create(model=DEPLOYMENT_NAME, input=text).data[0].embedding

df = pd.read_csv('data/out/abfall_abc_cleaned.csv')

points = []
for i, row in df.iterrows():
    text = row['Name']  # Only embed Name
    vec = embed(text)
    points.append({
        "id": i,
        "vector": vec,
        "payload": {
            "name": row["Name"],
            "abfallart": row["Abfallart"],
            "hinweis": row["Hinweis"]
        }
    })

# Upsert into Qdrant
requests.put(f"{QDRANT_URL}/collections/{COLLECTION}/points?wait=true",
             headers={"Content-Type": "application/json"},
             data=json.dumps({"points": points}))