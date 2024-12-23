from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
def get_data():
    return {"data": "This is data from data_api"}
