from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (access_project_update, check_name_duplicate,
                                check_project_exists, invested_in_project,
                                new_full_amount_greater)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_project(
    new_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(new_project.name, session)
    open_donations = await donation_crud.get_multi_by_attribute(
        'fully_invested', False, session
    )
    new_project = await charity_project_crud.create(
        session, new_project, commit=False
    )
    session.add_all(invest(new_project, open_donations))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partial_update_project(
    new_project: CharityProjectUpdate,
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)

    await access_project_update(project_id, session)
    await check_name_duplicate(new_project.name, session)
    await new_full_amount_greater(project_id, new_project.full_amount, session)
    updated_project = await charity_project_crud.update(
        session, project, new_project
    )
    return updated_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_projects(session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_multi(session)


@router.delete('/{project_id}', dependencies=[Depends(current_superuser)])
async def delete_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    await invested_in_project(project_id, session)
    charity_project_crud.remove(session, project)
    return project
