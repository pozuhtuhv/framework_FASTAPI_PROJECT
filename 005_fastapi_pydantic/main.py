from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import models
from database import engine
from routers import auth, posts

# app 기본설정
app = FastAPI()
# SQL class 속성 테이블 데이터베이스에 생성 서버는 database.py의 engine / 한번만 하면됨
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 연결
app.include_router(auth.router)
app.include_router(posts.router)

# 메인페이지 리다이렉트 설정
@app.get("/")
async def main():
    return RedirectResponse(url="/auth/", status_code=status.HTTP_303_SEE_OTHER)