from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    is_published:bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class ResponsePost(BaseModel):
    id:int
    title:str
    content:str
    is_published:bool
    created_at:datetime

    class config:
        orm_mode=True

class CreateResponsePost(BaseModel):
    id:int
    title:str
    created_at:datetime

    class config:
        orm_mode=True