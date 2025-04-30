from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.service import (
    transfer_of_donations, get_open_objects)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import (
    DonationCreate, DonationDBSuperUser, DonationDBUser)

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperUser],
    dependencies=[Depends(current_superuser)],
)
async def get_donation(
    session: AsyncSession = Depends(get_async_session)
):
    """Просмотр всех пожертвований доступен только суперпользователям."""
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.post('/', response_model=DonationDBUser)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Сделать пожертвование может любой пользователь."""
    open_projects = await get_open_objects(CharityProject, session)
    new_donation = await donation_crud.create(
        donation, session, user, flag=False)
    modified_objects = transfer_of_donations(new_donation, open_projects)
    session.add_all(modified_objects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationDBUser])
async def get_my_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Просмотр собственных пожертвований пользователем."""
    users_donation_list = await donation_crud.get_by_user(
        session=session, user=user)
    return users_donation_list
