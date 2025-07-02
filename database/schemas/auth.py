from pydantic import BaseModel,EmailStr
from datetime import datetime



class CreateUser(BaseModel):
    user_name:str
    email:EmailStr
    password:str

class LoginUser(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    user_name:str
    email:str
    created_at:datetime

    class config:
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str