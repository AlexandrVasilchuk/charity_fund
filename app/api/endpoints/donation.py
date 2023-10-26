from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBShort
from app.services.investments import invest

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
        session=session, obj_in=new_donation, user=user, commit=False
    )
    execute_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested.is_(False))
    )
    not_closed_projects = execute_projects.scalars().all()
    updated_investments = invest(donation, not_closed_projects)
    for instance in updated_investments:
        session.add(instance)

    await session.commit()
    await session.refresh(donation)
    return donation


@router.get('/my', response_model=list[DonationDBShort])
async def get_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_users_donation(user, session)
