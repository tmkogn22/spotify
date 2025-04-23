from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import models
from schemas import schemas
from datetime import datetime, timedelta
from database.async_db import get_db


PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = "HS256"
SECRET_KEY = 'oekwmd'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='users/login')


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


async def get_user(db: AsyncSession, email):
    async with db:
        result = await db.execute(select(models.User).filter(models.User.email == email))
        return result.scalar_one_or_none()


def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    data_copy = data.copy()
    expires_delta = datetime.utcnow() + expires_delta
    data_copy.update({'exp': expires_delta})
    encoded_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authentication_user(db: AsyncSession, email: str, password: str):
    user = await get_user(db, email)
    if user or verify_password(password, user.password_hash):
        return user
    return None


@router.post('/register/', response_model=schemas.User)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    new_password = PWD_CONTEXT.hash(user.password)
    db_user = models.User(email=user.email, password_hash=new_password, username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post('/login/', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authentication_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect email or password',
                            headers={'WWW-Authenticate': 'Bearer'})

    lifetime = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=lifetime
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user
