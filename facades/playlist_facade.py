from database import models
from facades.base_facade import BaseFacade
from fastapi import HTTPException, status
from schemas import schemas
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class PlaylistFacade(BaseFacade):
    async def create_playlist(self, user_id: int, playlist_data: schemas.PlaylistCreate) -> models.Playlist:
        playlist = models.Playlist(name=playlist_data.name, user_id=user_id)
        self.db.add(playlist)
        await self.db.commit()
        await self.db.refresh(playlist)
        return playlist

    async def add_comp_to_playlist(self,
                                   playlist_composition_data: schemas.PlaylistCompositionCreate) -> models.CompositionPlaylistAssociation:
        playlist = await self.db.get(models.Playlist, playlist_composition_data.playlist_id)

        if not playlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no such playlist')

        composition = await self.db.get(models.Composition, playlist_composition_data.composition_id)

        if not composition:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no such composition')

        existing = await self.db.execute(
            select(models.CompositionPlaylistAssociation).filter_by(playlist_id=playlist_composition_data.playlist_id,
                                                                    composition_id=playlist_composition_data.composition_id)
        )

        if existing.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='is already added')

        new_composition = models.CompositionPlaylistAssociation(
            playlist_id=playlist_composition_data.playlist_id,
            composition_id=playlist_composition_data.composition_id
        )

        self.db.add(new_composition)
        await self.db.commit()
        await self.db.refresh(new_composition)

        return new_composition

    async def get_all_playlist_compositions(self, user_id: int, playlist_id: int) -> schemas.PlaylistWithCompositions:
        result = await self.db.execute(
            select(models.Playlist).options(selectinload(models.Playlist.compositions).
                                            selectinload(models.CompositionPlaylistAssociation.composition)).
            filter_by(id=playlist_id, user_id=user_id)
        )

        result = result.scalar_one_or_none()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')

        compositions_data = [
            schemas.Composition
            .model_validate(playlist_composition.composition)
            .model_dump()
            for playlist_composition in result.compositions
        ]

        playlist_data = {
            "id": result.id,
            "user_id": result.user_id,
            "name": result.name,
            "compositions": compositions_data
        }

        return schemas.PlaylistWithCompositions(**playlist_data)

    async def view_all_playlists(self, user_id: int) -> list[schemas.Playlist]:
        result = await self.db.execute(select(models.Playlist).filter_by(user_id=user_id))

        result = result.scalars().all()

        return [schemas.Playlist.model_validate(playlist) for playlist in result]


playlist_facade = PlaylistFacade()
