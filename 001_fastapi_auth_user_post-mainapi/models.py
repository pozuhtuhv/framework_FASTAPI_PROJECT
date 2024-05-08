from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from database import Base


# 쿼리에 만들어질 열 정보 입력
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True)
    username = Column(String(30), unique=True)
    hashed_password = Column(String(500))
    role = Column(String(30))


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
