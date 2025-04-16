from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = (f'postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:'
                           f'{os.getenv('POSTGRES_PASSWORD')}@'
                           f'{os.getenv('POSTGRES_HOST')}/'
                           f'{os.getenv('POSTGRES_DB_NAME')}')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
