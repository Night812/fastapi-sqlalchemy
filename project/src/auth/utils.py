from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.token import TokenData
from src.core.models.db_helper import db_helper
from src.core.models.user import User
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.auth.access_token_expire_minutes,
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.auth.secret_key,
        algorithm=settings.auth.algorithm,
    )

    return encoded_jwt


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(
    session: AsyncSession,
    email: EmailStr,
) -> User:
    return await session.scalar(select(User).where(User.email == email))


async def authenticate_user(
    session: AsyncSession,
    email: EmailStr,
    password: str,
) -> User:
    user = await get_user(
        session=session,
        email=email,
    )

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


async def get_current_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    token: Annotated[str, Depends(oauth2_scheme)],
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=[
                settings.auth.algorithm,
            ],
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = await get_user(session=session, email=token_data.email)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_active:
        return current_user

    raise HTTPException(status_code=400, detail="Inactive user")
