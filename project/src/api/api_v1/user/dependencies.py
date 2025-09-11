from typing import Annotated
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from fastapi import Depends, HTTPException, status

from src.core.models.db_helper import db_helper
from src.core.models.user import User


async def user_by_email(
    email: EmailStr,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> User:
    user = await session.scalar(select(User).where(User.email == email))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


async def user_by_uuid(
    user_id: uuid.UUID,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> User:
    user = await session.scalar(select(User).where(User.user_id == user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
