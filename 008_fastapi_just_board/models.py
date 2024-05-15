# SQL 값에 대한 데이터 타입 설정
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

# 데이터베이스 테이블 매핑을 위한 모듈
from database import Base


# SQL 데이터베이스 Column, Datatype 설정
class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(30)) 
    title = Column(String(50))
    username = Column(String(30))
    description = Column(String(300))
    username = Column(String(50))
    post_time = Column(String(20))