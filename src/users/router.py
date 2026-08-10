from fastapi import APIRouter , Depends  , status
from src.users import controller
from src.users.dtos import UserSchema , UserResponseSchema , UserLoginResponseSchema , UserLoginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
router = APIRouter(prefix="/users")

@router.post("/register" , response_model=UserResponseSchema , status_code=status.HTTP_201_CREATED)
def register(body  : UserSchema , db :  Session = Depends(get_db) ):
    return controller.register(body , db )

# @router.post("/login", response_model=UserLoginResponseSchema , status_code=status.HTTP_200_OK)
@router.post("/login", status_code=status.HTTP_200_OK)
def register(body  : UserLoginSchema , db :  Session = Depends(get_db) ):
    return controller.login(body , db )
    
