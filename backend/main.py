from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from textwrap import fill

import os
import json
import requests
import uvicorn

# You can find your secret keys in the Azure portal (Azure Foundry) after creating an Azure OpenAI model deployment
# Make sure to set these environment variables in your deployment environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AZURE_OPENAI_API_ENDPOINT = os.environ.get("AZURE_OPENAI_API_ENDPOINT")
GPT_MODEL = "gpt-4o-mini-htw-test"
EMBED_MODEL = "text-embedding-3-small-htw-test"
QDRANT_URL = "http://localhost:6333"
COLLECTION = "abfall_docs"
WRAP_COLS = 100

class MessageInput(BaseModel):
    text: str

client = OpenAI(
    base_url=f"{AZURE_OPENAI_API_ENDPOINT}",
    api_key=OPENAI_API_KEY
)

app = FastAPI(title="Smart Recycle Bot API")

# Allow CORS for local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Helper functions ----------------
def embed_text(text: str):
    resp = client.embeddings.create(model=EMBED_MODEL, input=[text])
    return resp.data[0].embedding


def qdrant_search(
    vector,
    top_k: int,
):
    url = f"{QDRANT_URL}/collections/{COLLECTION}/points/search"
    body = {"vector": vector, "limit": top_k, "with_payload": True, "with_vector": False}
    r = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(body), timeout=30)
    if r.status_code >= 400:
        return []
    return r.json().get("result", [])


def format_hit(hit):
    """Extract category and explanation from a single Qdrant hit."""
    payload = hit.get("payload", {})
    return {
        "category": payload.get("abfallart", "Unknown"),
        "explanation": payload.get("hinweis", "")
    }


def format_hits(
    hits,
    min_score: float,
):
    """Format Qdrant search results for readable output."""
    if not hits:
        return "I don't know based on the available data."

    best_score = hits[0].get("score", 0.0)
    if best_score < min_score:
        return "I don't know based on the available data."

    lines = []
    for i, hit in enumerate(hits, start=1):
        payload = hit.get("payload", {}) or {}
        name = payload.get("name", f"Item {i}")
        abfallart = payload.get("abfallart", "")
        hinweis = payload.get("hinweis", "")

        lines.append(f"[{i}] {name} ({abfallart})")
        if hinweis:
            lines.append(fill(hinweis, width=WRAP_COLS))
        lines.append("")  # blank line between hits

    return "\n".join(lines).strip()


def summarize_hits(hits, user_question):
    """Always use GPT to generate human-like answer based on hits."""
    formatted_text = format_hits(hits, min_score=0.3)
    
    system_prompt = (
        "You are a helpful assistant that ONLY answers based on the provided information. "
        "If the information is insufficient, respond with: 'Ich weiß es nicht basierend auf den verfügbaren Daten.' "
        "Do not make up any content. Provide concise, human-readable answers in German."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {user_question}\n\nData:\n{formatted_text}"}
    ]

    try:
        resp = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            temperature=0
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # fallback to formatted hits if GPT fails
        return formatted_text

# ---------------- API Endpoints ----------------
@app.get("/")
async def root():
    return {"message": "Smart Recycle Bot is running"}

@app.post("/classify_text")
async def classify_text(message_input: MessageInput):
    try:
        query_vector = embed_text(message_input.text)
        hits = qdrant_search(query_vector, top_k=5)
        response_text = summarize_hits(hits, message_input.text)
        return {"response": response_text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

# ---------------- Run App ----------------
# Ensures this code only runs if the script is executed directly (not imported).
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/classify_image")
async def classify_image(file: UploadFile = File(...)):
    try:
        # Read image bytes
        img_bytes = await file.read()
        
        # Step 1: Use OpenAI to generate a description of the image
        vision_resp = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are an assistant that describes objects in images in a single word."},
                {"role": "user", "content": "Describe this image as a single object or product name."}
            ],
            temperature=0
        )
        # For simplicity, we assume GPT returns a product name like "Zahnbürste"
        description = vision_resp.choices[0].message.content.strip()
        
        # Step 2: Embed description and search Qdrant
        vector = embed_text(description)
        hits = qdrant_search(vector)
        if not hits or hits[0].get("score", 0.0) < MIN_SCORE:
            return {"category": "Unknown", "explanation": "No matching item found."}
        
        return format_hit(hits[0])
    
    except Exception as e:
        return {"category": "Unknown", "explanation": f"Error: {str(e)}"}
