from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserResponseSchema(BaseModel):
    id : int
    name: str
    username: str
    email: str
    # password: str

class UserLoginResponseSchema(BaseModel):
    token: str


    