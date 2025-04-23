from database import models
from facades.base_facade import BaseFacade
from schemas import schemas


class ArtistFacade(BaseFacade):

    async def create_artist(self, artist_data: schemas.ArtistCreate) -> models.Artist:
        db_artist = models.Artist(name=artist_data.name, description=artist_data.description)
        self.db.add(db_artist)
        await self.db.commit()
        await self.db.refresh(db_artist)
        return db_artist


artist_facade = ArtistFacade()
