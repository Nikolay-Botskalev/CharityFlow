from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Класс для реализации CRUD-операций."""

    def __init__(self, model):
        self.model = model

    async def get_multi(self, session: AsyncSession):
        """Получение списка объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession,
        user: Optional[User] = None, flag: bool = True
    ):
        """Создание объекта."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if flag:
            await session.commit()
            await session.refresh(db_obj)
        else:
            await session.flush()
        return db_obj

    async def update(
        self, db_obj, obj_in, session: AsyncSession, closing: bool = False
    ):
        """Обновление объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if closing:
            setattr(db_obj, 'fully_invested', True)
            setattr(db_obj, 'close_date', datetime.now())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self, db_obj, session: AsyncSession,
    ):
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
