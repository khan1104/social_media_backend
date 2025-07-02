from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto",bcrypt__rounds=12)

def hash_password(password: str):
    return pwd_context.hash(password)  

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)