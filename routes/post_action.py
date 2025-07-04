from fastapi import APIRouter,HTTPException,status,Depends
from database.models.post_actions import PostLikes,PostComments,Followers
from database.models.posts import Posts
from database.models.users import User
from config.database import get_db
from sqlalchemy.orm import Session
from auth.auth import get_current_user
from database.schemas.actions import Comment

router=APIRouter()


def find_user(user_id:int,db:Session):
    user=db.query(User).filter(User.id==user_id,User.is_deleted==False).first()
    if user:
        return user
    return None

def find(id:int,db:Session):
    data=db.query(Posts).filter(Posts.id == id,Posts.is_deleted==False).first()
    if data:
        return data
    return None

@router.post("/like",status_code=status.HTTP_200_OK)
def like(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    post=find(id,db)
    if post is None:
        raise HTTPException(detail="post not exists",status_code=status.HTTP_404_NOT_FOUND)
    like=db.query(PostLikes).filter(PostLikes.post_id==id,PostLikes.user_id==current_user.id).all()
    if like:
        raise HTTPException(detail="you already liked this post",status_code=status.HTTP_403_FORBIDDEN)
    
    liked=PostLikes(post_id=id,user_id=current_user.id)
    db.add(liked)
    db.commit()
    db.refresh(liked)

@router.post("/comment",status_code=status.HTTP_200_OK)
def comment(comment:Comment,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    post=find(comment.post_id,db)
    if post is None:
        raise HTTPException(detail="Post not exists",status_code=status.HTTP_404_NOT_FOUND)
    new_comment=PostComments(post_id=comment.post_id,user_id=current_user.id,text=comment.text)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

@router.post("/follow",status_code=status.HTTP_200_OK)
def follow(user_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    user=find_user(user_id,db)
    if user is None:
        raise HTTPException(detail="user not exists",status_code=status.HTTP_404_NOT_FOUND)
    follow=db.query(Followers).filter(Followers.follower_id==current_user.id,Followers.following_id==user_id).all()
    if follow:
        raise HTTPException(detail="you already follow this user",status_code=status.HTTP_403_FORBIDDEN)
    
    new_follow=Followers(follower_id=current_user.id,following_id=user_id)
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)




