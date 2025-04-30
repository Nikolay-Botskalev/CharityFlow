from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Класс для пожертвований."""

    async def get_by_user(self, user: User, session: AsyncSession):
        donation_list = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donation_list.scalars().all()


donation_crud = CRUDDonation(Donation)
