
from config.database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,TIMESTAMP,text,ForeignKey
from .base import TimestampMixin

class User(Base,TimestampMixin):
    __tablename__="users"
    id=Column(Integer,nullable=False,primary_key=True)
    user_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    is_verified=Column(Boolean,server_default=text("false"))