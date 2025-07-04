# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from typing import Optional
# from datetime import datetime, timedelta

# app = FastAPI()
# security = HTTPBearer()

# # Secret key and algorithm
# SECRET_KEY = "supersecretkey"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Dummy DB
# fake_users_db = {}

# # Password Hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Models
# class User(BaseModel):
#     username: str
#     password: str
#     role: str  # 'admin' or 'user'

# class UserInDB(User):
#     hashed_password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# def get_user(username: str):
#     user = fake_users_db.get(username)
#     if user:
#         return UserInDB(**user)

# async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user(username)
#     if user is None:
#         raise credentials_exception
#     return user

# # Routes
# @app.post("/register")
# def register(user: User):
#     if user.username in fake_users_db:
#         raise HTTPException(status_code=400, detail="User already exists")
#     hashed_password = get_password_hash(user.password)
#     fake_users_db[user.username] = {
#         "username": user.username,
#         "hashed_password": hashed_password,
#         "password": user.password,
#         "role": user.role
#     }
#     return {"msg": "User registered successfully"}

# @app.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     user = UserInDB(**user_dict)
#     if not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect password")
#     access_token = create_access_token(data={"sub": user.username, "role": user.role})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/create_user")
# def create_user(new_user: User, current_user: User = Depends(get_current_user)):
#     if current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Only admin can create users")
#     if new_user.username in fake_users_db:
#         raise HTTPException(status_code=400, detail="User already exists")
#     hashed_password = get_password_hash(new_user.password)
#     fake_users_db[new_user.username] = {
#         "username": new_user.username,
#         "hashed_password": hashed_password,
#         "password": new_user.password,
#         "role": new_user.role
#     }
#     return {"msg": f"User {new_user.username} created successfully"}

# @app.delete("/delete_user/{username}")
# def delete_user(username: str, current_user: User = Depends(get_current_user)):
#     if current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Only admin can delete users")
#     if username not in fake_users_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     del fake_users_db[username]
#     return {"msg": f"User {username} deleted successfully"}


from datetime import datetime,timedelta
from config.redis import redis_client


redis_client.set("name","1234")

data=redis_client.get("aman")
print(data)
# otps={}

# otps["khanirfan@gmail.com"]={"time":datetime.now()+timedelta(seconds=60),"otp":222}
# otps["khan@gmail.com"]={"time":datetime.now()+timedelta(seconds=60),"otp":2232}
# print(otps)

# # email=input("enter email:")
# # otp=int(input("enter the otp:"))

# def verify_otp(email,otp):
#     data=otps.get(email)

#     if data:
#         if data["time"] < datetime.now():
#             otps.pop(email)
#             print("❌ OTP expired")
#         elif data["otp"] == otp:
#             otps.pop(email)  # optional: remove after success
#             print("✅ Successful login")
#         else:
#             print("❌ Invalid OTP")
#     else:
#         print("❌ Email not found")
