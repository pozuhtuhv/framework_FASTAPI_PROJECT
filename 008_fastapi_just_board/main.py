import models
from database import engine
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from routers import posts
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles

app = FastAPI()
favicon_path = 'favicon.ico'
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

# html 디자인 및 파일 서비스 위치 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 경로 연결
app.include_router(posts.router)

# 메인페이지 리다이렉트 설정
@app.get("/")
async def main():
    return RedirectResponse(url="/posts", status_code=status.HTTP_303_SEE_OTHER)

# 차단할 IP 목록
blocked_ips = {"1.1.1.1"} # 1.1.1.1 의 아이피 차단
class BlockIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        if client_ip in blocked_ips:
            return templates.TemplateResponse("ipblock.html", {"request": request}, status_code=403)
        response = await call_next(request)
        return response

# Middleware 등록
app.add_middleware(BlockIPMiddleware)