from src.users.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException , status , Request
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.settings import settings
from src.utils.db import get_db
from fastapi import Depends

def is_authenticated(request  : Request, db : Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="you are unauthorized")
        token = token.split(" ")[-1]

        data = jwt.decode(token , settings.SECRET_KEY , settings.ALGORITHM)
        user_id = data.get("_id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="you are unauthorized")
        return user
    except InvalidTokenError:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="you are unauthorized")