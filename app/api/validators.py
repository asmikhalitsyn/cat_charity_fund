from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

NAME_OF_PROJECT_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_INVESTED = 'В проект были внесены средства, не подлежит удалению!'
SUM_LESS = 'Нельзя установить сумму ниже вложенной!'
CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
):
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_OF_PROJECT_EXISTS,
        )


def check_charity_project_already_invested(charity_project: CharityProject):
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_INVESTED
        )


def check_charity_project_invested_sum(project: CharityProject, new_amount: int):
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=SUM_LESS
        )


def check_charity_project_closed(charity_project: CharityProject):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CLOSED_PROJECT
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
):
    project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return project
