from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import session
from src.tasks.models import Task
def create_task(body : TaskSchema , db :session ):
    data = body.model_dump()
    new_task=  Task(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "create task route" , "data" : new_task}