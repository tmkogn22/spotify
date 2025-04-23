from fastapi import FastAPI
from database.async_db import get_db
from facades.artist_facade import artist_facade
from facades.album_facade import album_facade
from facades.genre_facade import genre_facade
from facades.composition_facade import composition_facade
from facades.favorite_composition_facade import favorite_composition_facade
from facades.playlist_facade import playlist_facade
from fastapi.security import OAuth2PasswordBearer
from apps.admin import admin
from apps.users import user
from apps.api import views

app = FastAPI()

OAUTH_SCHEME = OAuth2PasswordBearer('users/login/')


def set_all_facades(db):
    artist_facade.set_db(db)
    album_facade.set_db(db)
    genre_facade.set_db(db)
    composition_facade.set_db(db)
    favorite_composition_facade.set_db(db)
    playlist_facade.set_db(db)


@app.on_event('startup')
async def startup_event():
    async for db in get_db():
        set_all_facades(db)
        break


app.include_router(admin.router)
app.include_router(user.router)
app.include_router(views.router)


@app.get('/')
async def index():
    return {'message': 'hello'}
