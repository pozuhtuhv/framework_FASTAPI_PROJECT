import sys

sys.path.append("..")

from datetime import datetime
from math import ceil

import models
from database import get_db
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")

# pydantic 정의 ~51
class PostModel(BaseModel):
    title: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    description: str = Field(...)
def post_form_data(title: str = Form(...), username: str = Form(...), password: str = Form(...), description: str = Form(...)):
    return PostModel(title=title, username=username, password=password, description=description)

class EditModel(BaseModel):
    post_id: int
    title: str = Field(...)
    action: str = Field(...)
    password: str = Field(...)
    description: str = Field(...)
def edit_form_data(post_id: int, title: str = Form(...), action: str = Form(...), password: str = Form(...), description: str = Form(...)):
    return EditModel(post_id=post_id, title=title, action=action, password=password, description=description)

class DelModel(BaseModel):
    password: str = Field(..., min_length=1, max_length=30)

def del_form_data(password: str = Form(...)):
    return DelModel(password=password)


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    msg = request.query_params.get('msg', '')
    posts = db.query(models.Posts).order_by(desc(models.Posts.id)).all()
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "msg": msg})

# 글쓰기 템플릿 연결 
@router.get("/add-post", response_class=HTMLResponse)
async def add_new_post(request: Request):
    msg = request.query_params.get('msg', '')
    return templates.TemplateResponse("add-post.html", {"request": request, "msg": msg})

# 글쓰기 데이터 전송
@router.post("/add-post", response_class=HTMLResponse)
async def create_post(request: Request, post_data: PostModel = Depends(post_form_data), db: Session = Depends(get_db)):
    
    post_model = models.Posts()
    post_model.title = post_data.title
    post_model.description = post_data.description
    post_model.username = post_data.username
    post_model.password = post_data.password
    post_model.post_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    db.add(post_model)
    db.commit()

    return RedirectResponse(url="/posts?msg=Post updated successfully", status_code=status.HTTP_302_FOUND)

# 글수정 템플릿 연결
@router.get("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int, db: Session = Depends(get_db)):

    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    return templates.TemplateResponse("edit-post.html", {"request": request, "post": post})

# 글수정 및 삭제 데이터 전송
@router.post("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post(post_id: int, edit_data: EditModel = Depends(edit_form_data), db: Session = Depends(get_db)):
    # post_id에 해당하는 게시글 조회
    post_model = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if not post_model:
        raise HTTPException(status_code=404, detail="Post not found")

    # 비밀번호 확인
    if post_model.password != edit_data.password:
        # 비밀번호가 일치하지 않으면 메시지와 함께 리디렉트
        return RedirectResponse(url=f"/posts?msg=Password incorrect", status_code=status.HTTP_303_SEE_OTHER)
    
    if edit_data.action == "edit":
        # 게시글 수정
        post_model.title = edit_data.title
        post_model.description = edit_data.description
        db.commit()
        return RedirectResponse(url="/posts?msg=Post edited successfully", status_code=status.HTTP_302_FOUND)
    elif edit_data.action == "delete":
        # 게시글 삭제
        db.delete(post_model)
        db.commit()
        return RedirectResponse(url="/posts?msg=Post deleted successfully", status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

# 글조회 템플릿 연결
@router.get("/read-post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int, db: Session = Depends(get_db)):

    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    return templates.TemplateResponse("read-post.html", {"request": request, "post": post, "msg": post.title+" Read"})