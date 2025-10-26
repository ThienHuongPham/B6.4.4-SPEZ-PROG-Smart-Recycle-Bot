# Smart Recycle Bot Project

## Summary
Smart Recycle Bot is an AI-powered assistant that helps users classify waste correctly. Users can either describe the item in text or upload a picture. The AI then provides guidance on the proper disposal category. 

## Technical Description
- AI: OpenAI GPT-4o-mini and text-embedding-3-small (From Azure OpenAI)
- Backend: FastAPI with endpoints for text and image input.  
- Frontend: Streamlit for web interface.  
- Qdrant: Vector database
- Containerization: Docker + Kubernetes

## Setup steps (running locally before Docker + K8s)
- Download Python 3.11
- Create .venv in the highest level of the project folder
- Save credentials to environment variables
- Run BE: `fastapi dev backend/main.py` and access at http://localhost:8000/
- Run FE: `streamlit run frontend/main.py` and access at http://localhost:8501/

### How to manage packages: 
- `.venv\Scripts\activate`: activate the virtual env
- `pip install`: install new packages
- `pip freeze > requirements.txt`: create or update packages requirement based on .venv
- `deactivate`: Returns to the system Python

## Notes:
- Swagger UI is FastAPI’s auto-generated API docs at http://localhost:8000/docs
- CORS middleware (Cross-Origin Resource Sharing): Web browsers restrict frontend JavaScript from calling a backend on a different origin by default. Here Streamlit runs on localhost:8501 and backend runs on localhost:8000. CORS middleware allows FE to call the backend API without being blocked by the browser.
    - "*" allows any origin to call BE. In production you should restrict it to FE domain for security (Here: localhost).
    - allow_methods=["*"] → allow all HTTP methods (GET, POST, etc.)
    - allow_headers=["*"] → allow all headers
- A Pydantic model is a way in FastAPI (and other Python apps) to define the expected structure of input data (and output data). It ensures that the data you receive is valid and automatically parses JSON into Python objects.

## How to check data in Qdrant collection:
- Open Git bash
```
bash
 curl -X POST "http://localhost:6333/collections/abfall_docs/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{"limit": 3, "with_payload": true, "with_vector": false}'
```
- Or check structure inside running Qdrant container: `docker exec -it qdrant bash`

## General idea
1) Retrieve top hits from Qdrant.
2) Format them nicely using format_hits — this ensures consistent content structure, line breaks, sources, etc.
3) Feed the formatted text + user question to GPT-4o-mini to generate a natural, readable answer.
4) Return the GPT output to the user.
