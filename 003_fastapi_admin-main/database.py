from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# MYSQL 데이터베이스 연결
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:aaaaa@127.0.0.1:3306/fastapi_test"

# engine 데이터베이스
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# get_db 함수 지정
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()