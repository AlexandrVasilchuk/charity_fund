from typing import TypeVar, Union

from sqlalchemy import update

from app.core.db import AsyncSession, Base
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation

ModelType = TypeVar('ModelType', bound=Base)


async def investments(session: AsyncSession):
    while (
        await donation_crud.get_by_attribute('fully_invested', False, session)
        is not None
    ):
        donation = await donation_crud.get_by_attribute(
            'fully_invested', False, session
        )
        project = await charity_project_crud.get_by_attribute(
            'fully_invested', False, session
        )
        if project is None:
            break

        amendment = min(
            donation.full_amount - donation.invested_amount,
            project.full_amount - project.invested_amount,
        )
        project_data = generate_update_data(project, amendment)
        donation_data = generate_update_data(donation, amendment)
        await update_model(session, CharityProject, project, project_data)
        await update_model(session, Donation, donation, donation_data)
        await session.commit()


def generate_update_data(
    model: Union[CharityProject, Donation], amendment: int
) -> dict[str, Union[int, bool]]:
    update_data = {'invested_amount': model.invested_amount + amendment}
    if model.full_amount - model.invested_amount == amendment:
        update_data['fully_invested'] = True
    return update_data


async def update_model(session, model, db_object, update_data) -> None:
    await session.execute(
        update(model).where(model.id == db_object.id), [update_data]
    )
