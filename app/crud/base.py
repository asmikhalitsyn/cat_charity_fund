from typing import Optional, Union, List
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.charity_project import CharityProject
from app.models.donation import Donation


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
            commit: bool = True
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_full_invested_objects(
            self,
            session: AsyncSession,
            obj_in
    ) -> List[Union[CharityProject, Donation]]:
        objects = await session.execute(
            select(obj_in).where(obj_in.fully_invested == 0
                                 ).order_by(obj_in.create_date)
        )
        return objects.scalars().all()
