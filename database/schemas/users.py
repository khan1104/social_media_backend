
from pydantic import BaseModel,EmailStr
from datetime import datetime

class BaseUser(BaseModel):
    user_name:str
    email:EmailStr
    password:str

class CreateUser(BaseUser):
    pass

class UpdateUser(BaseUser):
    pass


class UserResponse(BaseModel):
    id:int
    user_name:str
    email:str
    created_at:datetime

    class config:
        orm_mode=True
