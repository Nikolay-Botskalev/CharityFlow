from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.service import (
    transfer_of_donations, get_open_objects)
from app.api.validators import (
    check_name_duplicate, сhecking_new_amount, check_project_exists,
    check_project_is_close, check_project_is_not_empty)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import project_crud
from app.models import Donation
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать проект может только суперпользователь."""
    await check_name_duplicate(project.name, session)
    open_donations = await get_open_objects(Donation, session)
    new_project = await project_crud.create(project, session, flag=False)
    modified_objects = transfer_of_donations(new_project, open_donations)
    session.add_all(modified_objects)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get('/', response_model=list[CharityProjectDB])
async def get_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Просмотр списка проектов доступен всем пользователям."""
    return await project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partial_update_project(
    project_id: int,
    new_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Изменять проект может только суперпользователь."""
    project = await check_project_exists(project_id, session)
    await check_project_is_close(project_id, session)

    if new_data.name:
        await check_name_duplicate(new_data.name, session)

    if new_data.full_amount is not None:
        await сhecking_new_amount(project_id, new_data.full_amount, session)

        if new_data.full_amount == project.invested_amount:
            project = await project_crud.update(
                project, new_data, session, closing=True)
            return project

    project = await project_crud.update(project, new_data, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить проект может только суперпользователь."""
    project = await check_project_exists(
        project_id, session
    )
    await check_project_is_close(project_id, session)
    await check_project_is_not_empty(project_id, session)
    return await project_crud.remove(project, session)
