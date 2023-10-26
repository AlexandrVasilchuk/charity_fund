from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User

from app.schemas.donation import DonationCreate, DonationDB, DonationDBShort
from app.services.investments import investments

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[
        Depends(current_superuser),
    ],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    '/', response_model=DonationDBShort, response_model_exclude_none=True
)
async def create_donation(
    *,
    session: AsyncSession = Depends(get_async_session),
    new_donation: DonationCreate,
    user: User = Depends(current_user)
):
    donation = await donation_crud.create(
        session=session, new_donation=new_donation, user=user
    )
    await investments(session)
    await session.refresh(donation)
    return donation


@router.get('/my', response_model=list[DonationDBShort])
async def get_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_users_donation(user, session)
