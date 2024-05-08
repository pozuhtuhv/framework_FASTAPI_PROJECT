import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    posts = db.query(models.Posts).filter(models.Posts.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "user": user})

# 글쓰기 템플릿 연결 
@router.get("/add-post", response_class=HTMLResponse)
async def add_new_post(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-post.html", {"request": request, "user": user})

# 글쓰기 데이터 전송
@router.post("/add-post", response_class=HTMLResponse)
async def create_post(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    post_model = models.Posts()
    post_model.title = title
    post_model.description = description
    post_model.priority = priority
    post_model.complete = False
    post_model.owner_id = user.get("id")

    db.add(post_model)
    db.commit()

    return RedirectResponse(url="/posts", status_code=status.HTTP_302_FOUND)

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
async def edit_post_commit(request: Request, post_id: int, title: str = Form(...),
                           description: str = Form(...), priority: int = Form(...),
                           db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    post_model = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    post_model.title = title
    post_model.description = description
    post_model.priority = priority

    db.add(post_model)
    db.commit()

    return RedirectResponse(url="/posts", status_code=status.HTTP_302_FOUND)

# 글삭제 데이터 전송
@router.get("/delete/{post_id}")
async def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    post_model = db.query(models.Posts).filter(models.Posts.id == post_id)\
        .filter(models.Posts.owner_id == user.get("id")).first()

    if post_model is None:
        return RedirectResponse(url="/posts", status_code=status.HTTP_302_FOUND)

    db.query(models.Posts).filter(models.Post.id == post_id).delete()

    db.commit()

    return RedirectResponse(url="/posts", status_code=status.HTTP_302_FOUND)

# todos 에서 적용 안적용이었는데 수정예정
@router.get("/complete/{post_id}", response_class=HTMLResponse)
async def complete_post(request: Request, post_id: int, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    post.complete = not post.complete

    db.add(post)
    db.commit()

    return RedirectResponse(url="/posts", status_code=status.HTTP_302_FOUND)
