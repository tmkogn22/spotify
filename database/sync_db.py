from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = (f'postgresql://{os.getenv('POSTGRES_USER')}:'
                           f'{os.getenv('POSTGRES_PASSWORD')}@'
                           f'{os.getenv('POSTGRES_HOST')}/'
                           f'{os.getenv('POSTGRES_DB_NAME')}')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
