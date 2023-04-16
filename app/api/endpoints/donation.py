from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationBase, DonationCreate, DonationDB
from app.services.invest import investing_process

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation,
        session,
        user,
        commit=False
    )
    model_objects = await donation_crud.get_not_full_invested_objects(
        session,
        CharityProject
    )
    if model_objects:
        session.add_all(investing_process(new_donation, model_objects))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationCreate],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(
        session=session, user=user
    )
