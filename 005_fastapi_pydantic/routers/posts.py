import sys

sys.path.append("..")

from datetime import datetime
from math import ceil

import models
from database import get_db
from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from .auth import get_current_user

# API Swagger 태그
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")

# pydantic 정의 ~51
class PostModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=30, description="The title of the post")
    description: str = Field(..., min_length=1, description="The detailed description of the post")
def post_form_data(title: str = Form(...), description: str = Form(...)):
    return PostModel(title=title, description=description)

class EditModel(BaseModel):
    post_id: int
    title: str = Field(..., min_length=1, max_length=100, description="The title of the edit")
    description: str = Field(..., min_length=1, description="The detailed description of the edit")
    
def edit_form_data(post_id: int, title: str = Form(...), description: str = Form(...)):
    return EditModel(post_id=post_id, title=title, description=description)

class DelModel(BaseModel):
    post_id: int

def del_data(post_id: int):
    return DelModel(post_id=post_id)

# 로그인 후 home 이동 글 리스트 확인
@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db), page: int = Query(default=1, ge=1)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    # 페이지네이션
    page_size = 10
    skip = (page - 1) * page_size

    # 로그인 한유저가 같은지 필터링
    if user.get('role') == 'admin':
        total_count = db.query(models.Posts).count()
        posts = db.query(models.Posts).order_by(desc(models.Posts.id)).offset(skip).limit(page_size).all()
    else:
        total_count = db.query(models.Posts).filter(models.Posts.owner_id == user.get("id")).count()
        posts = db.query(models.Posts).filter(models.Posts.owner_id == user.get("id")).order_by(desc(models.Posts.id)).offset(skip).limit(page_size).all()
    total_pages = ceil(total_count / page_size)

    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "user": user, "page": page, "total_pages": total_pages})

# 글쓰기 템플릿 연결 
@router.get("/add-post", response_class=HTMLResponse)
async def add_new_post(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-post.html", {"request": request, "user": user})

# 글쓰기 데이터 전송
@router.post("/add-post", response_class=HTMLResponse)
async def create_post(request: Request, post_data: PostModel = Depends(post_form_data), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    post_model = models.Posts()
    post_model.title = post_data.title
    post_model.description = post_data.description
    post_model.username = user.get('username')
    post_model.post_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    post_model.owner_id = user.get("id")
    db.add(post_model)
    db.commit()

    return RedirectResponse(url="/posts/", status_code=status.HTTP_302_FOUND)

# 글수정 템플릿 연결
@router.get("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    return templates.TemplateResponse("edit-post.html", {"request": request, "post": post, "user": user})

# 글수정 데이터 전송
@router.post("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post_commit(request: Request, edit_data: EditModel = Depends(edit_form_data), db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    post_model = db.query(models.Posts).filter(models.Posts.id == edit_data.post_id).first()

    post_model.title = edit_data.title
    post_model.description = edit_data.description

    db.add(post_model)
    db.commit()

    return RedirectResponse(url="/posts/", status_code=status.HTTP_302_FOUND)

# 글삭제 데이터 전송
@router.get("/delete/{post_id}")
async def delete_post(request: Request, del_data: DelModel = Depends(del_data), db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    # 로그인 한유저가 같은지 필터링
    if user.get('role') == 'admin': # admin 이 아닐결우 필터링해서
        post_model = db.query(models.Posts).filter(models.Posts.id == del_data.post_id).first()
    else:
        post_model = db.query(models.Posts).filter(models.Posts.id == del_data.post_id).filter(models.Posts.owner_id == user.get("id")).first()
    if post_model is None:
        return RedirectResponse(url="/posts/", status_code=status.HTTP_302_FOUND)

    db.query(models.Posts).filter(models.Posts.id == del_data.post_id).delete()

    db.commit()

    return RedirectResponse(url="/posts/", status_code=status.HTTP_302_FOUND)