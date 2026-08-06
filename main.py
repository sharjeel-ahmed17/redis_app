from fastapi import FastAPI
from src.utils.db import engine, Base 

Base.metadata.create_all(engine)

app = FastAPI(title="this is my task managment application")

@app.get("/")
def home():
    return {
        "message" : "api is running fine"
    }
