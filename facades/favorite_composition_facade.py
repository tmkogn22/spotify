from database import models
from facades.base_facade import BaseFacade
from fastapi import HTTPException, status
from schemas import schemas
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class FavoriteFacade(BaseFacade):

    async def like_composition(self, composition_id: int, user_id: int) -> schemas.FavoriteComposition:
        composition = await self.db.get(models.Composition, composition_id)

        if not composition:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no such composition')

        existing_like = await self.db.execute(
            select(models.Favorites).filter_by(user_id=user_id, composition_id=composition_id)
        )

        if existing_like.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='is already liked')

        favorite = models.Favorites(user_id=user_id, composition_id=composition_id)
        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)

        return favorite

    async def get_all_favorites(self, user_id: int) -> list[schemas.Composition]:
        favorites = await self.db.execute(
            select(models.Favorites).filter_by(user_id=user_id).options(selectinload(models.Favorites.composition))
        )

        favorites = favorites.scalars().all()

        return [composition.composition for composition in favorites]


favorite_composition_facade = FavoriteFacade()
