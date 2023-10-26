from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    async def create(
        self, session: AsyncSession, new_donation: DonationCreate, user: User
    ):
        donation_in_data = new_donation.dict()
        donation_in_data['user_id'] = user.id
        new_donation = self.model(**donation_in_data)
        session.add(new_donation)
        await session.commit()
        await session.refresh(new_donation)
        return new_donation

    async def get_users_donation(self, user: User, session: AsyncSession):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
