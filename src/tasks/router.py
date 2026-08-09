from fastapi import APIRouter , Depends , status
from src.tasks import controller
from src.tasks.dtos import TaskSchema , TaskResponseSchema
from src.utils.db import get_db
from sqlalchemy.orm import session
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/" , response_model=TaskResponseSchema , status_code=status.HTTP_201_CREATED)
def create_task(body : TaskSchema , db : session = Depends(get_db) ):
    return controller.create_task(body , db )
@router.get("/" , response_model=List[TaskResponseSchema] , status_code=status.HTTP_200_OK)
def get_all_task(db : session = Depends(get_db)):
    return controller.get_task(db)
@router.get("/{task_id}", response_model=TaskResponseSchema , status_code=status.HTTP_200_OK)
def get_single_task(task_id : int , db : session = Depends(get_db)):
    return controller.get_single_task(task_id, db)
@router.put("/{task_id}", response_model=TaskResponseSchema , status_code=status.HTTP_201_CREATED)
def update_task(body: TaskSchema , task_id : int, db : session = Depends(get_db)):
    return controller.update_task(body , task_id , db )
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task( task_id: int , db : session = Depends(get_db)):
    return controller.update_task(task_id , db )