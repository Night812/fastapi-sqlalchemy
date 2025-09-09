from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.user.schemas import ShowUser, UserCreate, UserUpdate
from core.models import User, db_helper
from auth.utils import get_current_active_user
from .dependencies import user_by_email
from . import crud


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[ShowUser])
async def get_users(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.get_users(session)


@router.post("/", response_model=ShowUser)
async def create_user(
    user: UserCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.create_user(
        user=user,
        session=session,
    )


@router.get("/{email}", response_model=ShowUser)
async def get_user_by_email(
    user: Annotated[User, Depends(user_by_email)],
):
    return user


@router.patch("/{email}", response_model=ShowUser)
async def patch_user_by_email(
    new_data: UserUpdate,
    user: Annotated[User, Depends(user_by_email)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):

    return await crud.update_user_partial(
        data=new_data,
        user=user,
        session=session,
    )


@router.delete("/{email}", status_code=204)
async def delete_user_by_email(
    # current_user: Annotated[
    #     User,
    #     Depends(get_current_active_user),
    # ],
    user: Annotated[
        User,
        Depends(user_by_email),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    await crud.delete_user(
        user=user,
        session=session,
    )
