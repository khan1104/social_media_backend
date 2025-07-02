from config.database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,TIMESTAMP,text,ForeignKey
from .base import TimestampMixin

class Posts(Base,TimestampMixin):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    media_url=Column(String,nullable=True)
    is_published=Column(Boolean,nullable=False,server_default=text("true"))
    created_by=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)