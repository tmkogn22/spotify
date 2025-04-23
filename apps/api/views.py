from database import models
from schemas import schemas
from fastapi import Depends, APIRouter
from database.async_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from apps.users.user import get_current_user
from facades.favorite_composition_facade import favorite_composition_facade
from facades.playlist_facade import playlist_facade


router = APIRouter(
    prefix='/api',
    tags=['API']
)


@router.post('/favorites/', response_model=schemas.FavoriteComposition)
async def like_composition(
        composition_data: schemas.FavoriteCompositionCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    favorite_composition = await favorite_composition_facade.like_composition(
        composition_id=composition_data.composition_id,
        user_id=current_user.id
    )

    return favorite_composition


@router.get('/favorites/', response_model=list[schemas.Composition])
async def gat_all_favorites(
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    favorites = await favorite_composition_facade.get_all_favorites(
        user_id=current_user.id
    )

    return favorites


@router.post('/playlists', response_model=schemas.Playlist)
async def create_playlist(
        playlist_data: schemas.PlaylistCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    playlist = await playlist_facade.create_playlist(user_id=current_user.id, playlist_data=playlist_data)

    return playlist


@router.post('/playlists/', response_model=schemas.PlaylistComposition)
async def add_composition_to_playlist(
        playlist_composition_data: schemas.PlaylistCompositionCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await playlist_facade.add_comp_to_playlist(playlist_composition_data=playlist_composition_data)

    return result


@router.get('/playlists/{playlist_id}/compositions/', response_model=schemas.PlaylistWithCompositions)
async def view_compositions_in_playlist(
        playlist_id: int,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await playlist_facade.get_all_playlist_compositions(user_id=current_user.id, playlist_id=playlist_id)

    return result


@router.get('/playlists/', response_model=list[schemas.Playlist])
async def view_all_playlists(current_user: models.User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):
    result = await playlist_facade.view_all_playlists(user_id=current_user.id)

    return result
