import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import httpx
from pydantic_models import YoutubeUrlInfo # Pour définir la forme des données de requête et de réponse
from pydantic import ValidationError
from mongo_utils import insert_yt_url_record, create_yt_url_store_index
from pymongo.errors import DuplicateKeyError

# # Initialisation MongoDB : création des index
# create_yt_url_store_index()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_yt_url_store_index()
    yield

app = FastAPI(lifespan=lifespan)

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
    Enregistre l'URL dans la base de données et renvoie un message.
    """
    try:
        # Appelle la fonction d'insertion
        result = insert_yt_url_record(info.url)
        if "id" in result:
            return {
                "url": info.url,
                "upload_timestamp": info.upload_timestamp,
                "message": "L'URL YouTube est valide et a été enregistrée."
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="L'URL YouTube est déjà enregistrée.")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="L'URL doit être une URL YouTube valide.")