from fastapi import FastAPI, HTTPException
import os
import httpx
from app_api.pydantic_models import YoutubeUrlInfo # Pour définir la forme des données de requête et de réponse


app = FastAPI()

DATA_API_URL = os.getenv("DATA_API_URL", "http://localhost:9000")

@app.get("/")
def read_root():
    return {"message": "Welcome to app_api!"}

@app.get("/fetch-data")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATA_API_URL}/data")
    return {"data_from_data_api": response.json()}


# Endpoint pour valider et renvoyer les informations sur une URL YouTube
@app.post("/youtube-url")
async def youtube_url(info: YoutubeUrlInfo):
    """
    Valide une URL YouTube et renvoie les informations associées.
    """
    try:
        return {
            "url": info.url,
            "upload_timestamp": info.upload_timestamp,
            "message": "L'URL YouTube est valide et a été acceptée."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
