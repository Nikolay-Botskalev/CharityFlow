from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDProject(CRUDBase):

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Функция проверяет наличие объекта с заданным именем в БД."""
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name))
        project_id = project_id.scalars().first()
        return project_id

    async def get(
        self, obj_id: int, session: AsyncSession
    ):
        """Получение отдельного объекта по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        objects = await session.execute(
            select(self.model).where(self.model.close_date is not None)
        )
        objects = objects.scalars().all()
        sorted_objects = sorted(
            objects, key=lambda x: x.close_date - x.create_date)
        return sorted_objects


project_crud = CRUDProject(CharityProject)
