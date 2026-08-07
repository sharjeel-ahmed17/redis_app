import json
from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import session
from src.tasks.models import Task
from src.utils.db import redis_client

TASKS_CACHE_KEY = "tasks"
CACHE_TTL = 60

def create_task(body : TaskSchema , db : session ):
    data = body.model_dump()
    new_task=  Task(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    redis_client.delete(TASKS_CACHE_KEY)
    return {"message": "create task route" , "data" : new_task}


def get_task(db : session):
    cached = redis_client.get(TASKS_CACHE_KEY)
    if cached:
        return {
            "messages": "get task (from cache)",
            "data": json.loads(cached)
        }

    tasks = db.query(Task).all()
    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
        }
        for task in tasks
    ]
    redis_client.setex(TASKS_CACHE_KEY, CACHE_TTL, json.dumps(tasks_data))
    return {
        "messages" : "get task",
        "data" : tasks_data
    }


