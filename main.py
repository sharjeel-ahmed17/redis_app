from fastapi import FastAPI 
from src.utils.db import engine, Base 
# from src.tasks.models import Task
from src.tasks.router import router
Base.metadata.create_all(engine)

app = FastAPI(title="this is my task managment application")

@app.get("/")
def home():
    return {
        "message" : "api is running fine"
    }
app.include_router(router)