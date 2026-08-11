from fastapi import APIRouter , Depends  , status , Request , BackgroundTasks
from src.users import controller
from src.users.dtos import UserSchema , UserResponseSchema , UserLoginResponseSchema , UserLoginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
router = APIRouter(prefix="/users" , tags=["users"])

@router.post("/register" , response_model=UserResponseSchema , status_code=status.HTTP_201_CREATED)
async def register(body  : UserSchema , bg_task : BackgroundTasks , db :  Session = Depends(get_db)  ):
    return await controller.register(body , db , bg_task )

@router.post("/login" ,response_model=UserLoginResponseSchema , status_code=status.HTTP_200_OK)
def login(body  : UserLoginSchema , db :  Session = Depends(get_db) ):
    return controller.login(body , db )

@router.get("/is-authenticated",response_model=UserResponseSchema , status_code=status.HTTP_200_OK)
def is_authenticated(request : Request, db :  Session = Depends(get_db) ):
    return controller.is_authenticated(request  , db )
    
