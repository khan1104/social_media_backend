

from config.database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,TIMESTAMP,text,ForeignKey

class PostLikes(Base):

    #using two primary key we make this as composit key so that each row have different values user cannot like post multiple times

    __tablename__="post_likes"
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

class Followers(Base):
    #using two primary key we make this as composit key so that each row have different values user cannot follow same user many times
    __tablename__="followers"
    follower_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    following_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

class PostComments(Base):
    __tablename__="post_commnets"
    id=Column(Integer,primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    text=Column(Text,nullable=False)