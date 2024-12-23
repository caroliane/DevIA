from fastapi import FastAPI
import os
import httpx

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
