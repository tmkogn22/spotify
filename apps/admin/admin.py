from database import models
from schemas import schemas
from facades.artist_facade import artist_facade
from facades.album_facade import album_facade
from facades.genre_facade import genre_facade
from facades.composition_facade import composition_facade
from facades.file_facade import FILE_MANAGER
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from apps.users.user import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.post('/artists/', response_model=schemas.Artist)
async def create_artist(
        artist_data: schemas.ArtistCreate, current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not allowed to")

    db_artist = await artist_facade.create_artist(artist_data=artist_data)
    return db_artist


@router.post('/albums/', response_model=schemas.Album)
async def create_album(
        album_data: schemas.AlbumCreate, current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not allowed to")

    db_album = await album_facade.create_album(album_data=album_data)
    return db_album


@router.post('/genres/', response_model=schemas.Genre)
async def create_genre(
        genre_data: schemas.GenreCreate, current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not allowed to")

    db_genre = await genre_facade.create_genre(genre_data=genre_data)
    return db_genre


@router.post('/compositions/', response_model=schemas.Composition)
async def create_composition(
        title: str = Form(...),
        lyrics: str = Form(...),
        album_id: int = Form(...),
        file: UploadFile = File(...),
        genres: str = Form(...),
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not allowed to")
    file_path = f'static/compositions/{file.filename}'
    await FILE_MANAGER.save_file(file, file_path)

    genres_list = [int(genre_id) for genre_id in genres.split(',')]
    composition = schemas.CompositionCreate(
        title=title,
        lyrics=lyrics,
        album_id=album_id,
        genres=genres_list
    )

    db_composition = await composition_facade.create_composition(composition, file_path)
    return db_composition
