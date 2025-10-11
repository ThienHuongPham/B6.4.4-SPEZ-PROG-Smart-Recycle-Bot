from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
import os

# You can find your secret keys in the Azure portal (Azure Foundry) after creating an Azure OpenAI model deployment
# Make sure to set these environment variables in your deployment environment
api_key = os.environ.get("OPENAI_API_KEY")
endpoint = os.environ.get("AZURE_OPENAI_API_ENDPOINT")
deployment_name = "gpt-4o-mini-htw-test"

class MessageInput(BaseModel):
    text: str

client = OpenAI(
    base_url=f"{endpoint}",
    api_key=api_key
)

app = FastAPI(title="Smart Recycle Bot API")

# Allow CORS for local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/classify_text")
async def classify_text(message_input: MessageInput):
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful bot helping users to classify waste items into recycling categories."},
            {"role": "user", "content": message_input.text}
        ],
    )
    return {"response": response.choices[0].message.content}
