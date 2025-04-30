from datetime import datetime
from typing import Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_open_objects(
    model: Type[Union[CharityProject, Donation]],
    session: AsyncSession
):
    result = await session.execute(
        select(model).where(
            model.fully_invested == False,  # noqa
            model.close_date.is_(None)))
    return result.scalars().all()


def closing_object(obj: Union[CharityProject, Donation]) -> None:
    obj.close_date = datetime.now()
    obj.fully_invested = True


def transfer_of_donations(
    target: Union[CharityProject, Donation],
    sources: list[Union[CharityProject, Donation]]
) -> list[Union[CharityProject, Donation]]:
    modified_objects = []
    for source in sources:
        required_amount = target.full_amount - target.invested_amount
        free_amount = source.full_amount - source.invested_amount
        invested_summ = min(required_amount, free_amount)

        source.invested_amount += invested_summ
        target.invested_amount += invested_summ

        if source.invested_amount == source.full_amount:
            closing_object(source)

        if target.invested_amount == target.full_amount:
            closing_object(target)
            break
        modified_objects.append(source)

    modified_objects.append(target)
    return modified_objects
