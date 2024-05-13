from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, FileResponse
import models
from database import engine
from routers import auth, posts
from starlette.staticfiles import StaticFiles

app = FastAPI()
favicon_path = 'favicon.ico'

models.Base.metadata.create_all(bind=engine)

# html 디자인 및 파일 서비스 위치 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 경로 연결
app.include_router(auth.router)
app.include_router(posts.router)

# 메인페이지 리다이렉트 설정
@app.get("/")
async def main():
    return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)