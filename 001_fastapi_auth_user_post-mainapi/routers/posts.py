from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Posts

from .auth import get_current_user  # 같은 폴더 내 auth.py의 get_current_user 함수 사용

# Swagger 태그 설정 아무것도 없으니 default tag에 들어감
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 연결
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Request date
class PostRequest(BaseModel):
    title: str = Field(min_length=3, max_length=40) # 최소, 최대 설정
    description: str = Field(min_length=3, max_length=100) # 최소, 최대글자 설정

# 포스트 전체 출력
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Posts).filter(Posts.owner_id == user.get('id')).all()

# 포스트 지정 출력
@router.get("/post/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(user: user_dependency, db: db_dependency, post_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    post_model = db.query(Posts).filter(Posts.id == post_id)\
        .filter(Posts.owner_id == user.get('id')).first()
    if post_model is not None:
        return post_model
    raise HTTPException(status_code=404, detail='post not found.')

# 포스트 -> 업로드
@router.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(user: user_dependency, db: db_dependency,
                      post_request: PostRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    post_model = Posts(**post_request.model_dump(), owner_id=user.get('id'))

    db.add(post_model)
    db.commit()

# 포스트 지정 수정
@router.put("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(user: user_dependency, db: db_dependency,
                      post_request: PostRequest,
                      post_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    post_model = db.query(Posts).filter(Posts.id == post_id)\
        .filter(Posts.owner_id == user.get('id')).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail='post not found.')

    post_model.title = post_request.title
    post_model.description = post_request.description

    db.add(post_model)
    db.commit()

# 포스트 지정 삭제
@router.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(user: user_dependency, db: db_dependency, post_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    post_model = db.query(Posts).filter(Posts.id == post_id)\
        .filter(Posts.owner_id == user.get('id')).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail='post not found.')
    db.query(Posts).filter(Posts.id == post_id).filter(Posts.owner_id == user.get('id')).delete()

    db.commit()












