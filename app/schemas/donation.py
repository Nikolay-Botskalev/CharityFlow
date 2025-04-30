# app/schemas/donation.py
from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: int = Field(..., ge=1)


class DonationCreate(DonationBase):
    pass


class DonationDBUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperUser(DonationDBUser):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
