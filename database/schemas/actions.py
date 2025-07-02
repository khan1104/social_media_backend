from pydantic import BaseModel

class Comment(BaseModel):
    post_id:int
    text:str