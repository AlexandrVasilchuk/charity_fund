from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


PROJECT_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_ALREADY_CLOSED = 'Закрытый проект нельзя редактировать!'
PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению!'
)
PROJECT_FULL_AMOUNT_INCORRECT = 'Новая сумма не может быть меньше предыдущей'


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get_by_attribute(
        'name', project_name, session
    )
    if project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_EXISTS,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


async def access_project_update(
    project_id: int, session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_ALREADY_CLOSED,
        )
    return project


async def invested_in_project(project_id: int, session: AsyncSession) -> None:
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_HAS_INVESTMENTS,
        )


async def new_full_amount_greater(
    project_id: int, new_full_amount: int, session: AsyncSession
) -> None:
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if new_full_amount and new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_FULL_AMOUNT_INCORRECT,
        )
