from fastapi import APIRouter , Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/")
def create_task(body : TaskSchema , db = Depends(get_db) ):
    return controller.create_task(body , db )


@router.get("/")
def get_all_task(db = Depends(get_db)):
    return controller.get_task(db)
@router.get("/{task_id}")
def get_single_task(task_id : int , db = Depends(get_db)):
    return controller.get_single_task(task_id, db)