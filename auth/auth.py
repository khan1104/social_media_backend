from jose import jwt, JWTError
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from database.models.users import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security=HTTPBearer()
def create_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=30)  
    to_encode.update({"exp": expire_time})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return token


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    id = verify_token(token.credentials, credentials_exception)
    
    user = db.query(User).filter(User.email == id, User.is_deleted == False).first()
    
    if user is None:
        raise credentials_exception
    return user