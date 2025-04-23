from database import models
from facades.base_facade import BaseFacade
from schemas import schemas


class CompositionFacade(BaseFacade):

    async def create_composition(self, composition_data: schemas.CompositionCreate,
                                 file_path: str) -> models.Composition:
        db_composition = models.Composition(title=composition_data.title,
                                            lyrics=composition_data.lyrics,
                                            album_id=composition_data.album_id,
                                            file_path=file_path)
        self.db.add(db_composition)
        await self.db.commit()
        await self.db.refresh(db_composition)

        for genre_id in composition_data.genres:
            genre = await self.db.get(models.Genre, genre_id)
            if genre:
                comp_genre = models.CompositionGenreAssociation(composition_id=db_composition.id, genre_id=genre_id)
                self.db.add(comp_genre)

        await self.db.commit()
        await self.db.refresh(db_composition)

        return db_composition


composition_facade = CompositionFacade()
