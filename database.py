from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:cvs2677@localhost/TodoApplicationDatabase'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:cvs2677@127.0.0.1:3306/TodoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
