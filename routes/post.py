
from fastapi import APIRouter,HTTPException,Depends,status
from database.models.posts import Posts
from database.schemas.posts import CreatePost,ResponsePost,CreateResponsePost,UpdatePost

from config.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

from auth.auth import get_current_user

router=APIRouter()

def find(id:int,db:Session):
    data=db.query(Posts).filter(Posts.id == id).first()
    if data:
        return data
    return None

@router.get("/posts",status_code=status.HTTP_200_OK,response_model=list[ResponsePost])
def get_posts(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return db.query(Posts).filter(Posts.is_deleted==False,Posts.created_by==current_user.id).all()


@router.get("/posts/{id}",status_code=status.HTTP_200_OK,response_model=ResponsePost)
def get_post_by_id(id:int,db: Session = Depends(get_db)):
    post=find(id,db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    return post

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=CreateResponsePost)
def create_post(post:CreatePost,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    new_post = Posts(created_by=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/posts/{id}", response_model=ResponsePost, status_code=status.HTTP_200_OK)
def update_post(
    id: int,
    post: CreatePost,
    db: Session = Depends(get_db)
):
    existing_post = find(id,db)
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    existing_post.updated_at=datetime.now()
    for key, value in post.model_dump().items():
        setattr(existing_post, key, value)
    db.commit()
    db.refresh(existing_post)
    return existing_post

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db: Session = Depends(get_db)):
    post=find(id,db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    post.is_deleted=True
    db.commit()







