from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """
    Функция проверяет уникальность полученного имени проекта.
    При неуникальности имени вызывается ошибка 422.
    """

    room_id = await project_crud.get_project_id_by_name(project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Функция проверяет наличие элемента в БД по его id.
    При отсуствии проекта вызывается ошибка 404.
    """

    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_is_close(
    project_id: int,
    session: AsyncSession
) -> None:
    """
    Функция проверяет, закрыт ли проект.
    Если проект закрыт, вызывается ошибка 400.
    """

    project = await project_crud.get(project_id, session)
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект {project.name!r} закрыт!'
        )


async def check_project_is_not_empty(
    project_id: int,
    session: AsyncSession
) -> None:
    """
    Функция проверяет, были ли инвестированы средства в проект.
    Если в проекте имеются средства, вызывается ошибка 400.
    """

    project = await project_crud.get(project_id, session)
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить проект, в который инвестированы средства!'
        )


async def сhecking_new_amount(
    project_id: int,
    new_amount: int,
    session: AsyncSession
) -> None:
    """
    Функция сравнивает новое значение сбора с инвестированной в проект суммой.
    Если новая сумма сбора меньше инвестированной, вызывается ошибка 400.
    """

    project = await project_crud.get(project_id, session)
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение меньше уже вложенной суммы.'
        )
