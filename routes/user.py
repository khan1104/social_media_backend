from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from database.models.users import User
from database.schemas.users import UserResponse
from config.database import get_db
from sqlalchemy.orm import Session
from utils.password import hash_password,verify_password
from auth.auth import create_token,get_current_user

router=APIRouter()

def finduser(email:str,db:Session):
    user=db.query(User).filter(User.email == email,User.is_deleted==False).first()
    if user:
        return user
    return None

def finddeleteduser(email:str,db:Session):
    deleted_user=db.query(User).filter(User.email == email,User.is_deleted==True).first()
    if deleted_user:
        return deleted_user
    return None

@router.get("/user",status_code=status.HTTP_200_OK,response_model=list[UserResponse])
def get_all_user(db:Session=Depends(get_db),user_data=Depends(get_current_user)):
    #Id 1 is for admin
    if user_data.id!=1:
        raise HTTPException(detail="You cannot access this resources",status_code=status.HTTP_403_FORBIDDEN)
    return db.query(User).filter(User.is_deleted==False).all()

@router.get("/user/{email}",status_code=status.HTTP_200_OK,response_model=UserResponse)
def get_user(email:str,db:Session=Depends(get_db),user_data=Depends(get_current_user)):
    user=finduser(email,db)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with this email not found")
    return user_data


@router.delete("/delete/{email}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email:str,db:Session=Depends(get_db),user_data=Depends(get_current_user)):
    user=finduser(email,db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with this email not exists")
    user.is_deleted = True
    db.commit()
