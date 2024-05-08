from fastapi import FastAPI

import models
from database import engine
from routers import admin, auth, posts, users  # routers 폴더의 py 이용

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 각 기능의 router 이용
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(admin.router)
app.include_router(users.router)