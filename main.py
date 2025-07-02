from fastapi import FastAPI
from routes.post import router as post_router
from routes.user import router as user_router
from routes.post_action import router as action_router
from routes.auth import router as auth_router

from config.database import engine
from config.database import Base


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(post_router,prefix="/posts", tags=["Posts"])
app.include_router(user_router,prefix="/user", tags=["user"])
app.include_router(action_router,prefix="/actions",tags=["actions"])
app.include_router(auth_router,prefix="/auth",tags=["auth"])
@app.get("/")
def helath():
    return {"message":"hello from health"}