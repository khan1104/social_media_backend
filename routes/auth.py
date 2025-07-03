from fastapi import HTTPException,status,Depends,APIRouter
from config.database import get_db
from sqlalchemy.orm import Session
from database.models.users import User
from utils.password import verify_password,hash_password
from auth.auth import create_token,get_current_user
from utils.send_otp import send_email
from config.redis import redis_client
from utils.verify_otp import otp_storage,validate_otp
from datetime import datetime,timedelta

from database.schemas.auth import UserResponse,CreateUser,LoginUser,Token

router=APIRouter()


# opt_storage={}

def finduser(email:str,db:Session):
    user=db.query(User).filter(User.email == email,User.is_deleted==False,User.is_verified==True).first()
    if user:
        return user
    return None

def finddeleteduser(email:str,db:Session):
    deleted_user=db.query(User).filter(User.email == email,User.is_deleted==True).first()
    if deleted_user:
        return deleted_user
    return None

def find_not_verified_user(email:str,db:Session):
    user=db.query(User).filter(User.email == email,User.is_deleted==False,User.is_verified==False).first()
    if user:
        return user
    return None


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(data: CreateUser, db: Session = Depends(get_db)):
    data.email = data.email.lower().strip()
    deleted_user = finddeleteduser(data.email, db)
    if deleted_user:
        db.delete(deleted_user)
        db.commit()

    user = finduser(data.email, db)
    if user:
        raise HTTPException(status_code=409, detail="Email already present")

    not_verified_user=find_not_verified_user(data.email,db)
    if not_verified_user:
        db.delete(not_verified_user)
        db.commit()

    data.password = hash_password(data.password)
    new_user = User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
        
    otp = send_email(new_user.email)
    expr_time=datetime.now()+timedelta(seconds=60)
    otp_storage[new_user.email]={"time":expr_time,"otp":otp}
    return {"message": f"OTP sent to {new_user.email}, please verify it."}

@router.post("/verify", status_code=status.HTTP_200_OK, response_model=UserResponse)
def verify_otp(email: str, otp: int, db: Session = Depends(get_db)):
    email = email.lower().strip()
    user = find_not_verified_user(email,db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    validate_otp(email,otp)
    user.is_verified = True
    db.commit()
    return user

@router.post("/login", status_code=status.HTTP_200_OK,response_model=Token)
def user_login(data: LoginUser, db: Session = Depends(get_db)):
    user = finduser(data.email, db)
    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email first")

    token = create_token({"sub": user.id})
    return token

    