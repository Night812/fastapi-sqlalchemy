from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.api.api_v1.user.schemas import UserCreate, UserUpdate
from src.core.models.user import User
from src.core.models.portal_role import PortalRole
from src.auth.utils import get_password_hash


async def get_users(session: AsyncSession):
    users = await session.scalars(select(User))
    return users


async def create_user(
    user: UserCreate,
    session: AsyncSession,
):
    old_user = await session.scalar(select(User).where(User.email == user.email))

    if old_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"There's already a user with email {user.email}",
        )

    user.password = get_password_hash(user.password)
    new_user = User(
        **user.model_dump(),
        roles=(
            [
                PortalRole.ROLE_PORTAL_USER,
            ]
        ),
    )

    session.add(new_user)
    await session.commit()

    return new_user


async def update_user_partial(
    data: UserUpdate,
    user: User,
    session: AsyncSession,
):

    if data.password:
        data.password = get_password_hash(data.password)

    stmt = (
        update(User)
        .where(User.email == user.email)
        .values(**data.model_dump(exclude_none=True))
    )

    await session.execute(stmt)
    await session.commit()
    await session.flush(user)

    return user


async def delete_user(
    user: User,
    session: AsyncSession,
):
    await session.delete(user)
    await session.commit()
