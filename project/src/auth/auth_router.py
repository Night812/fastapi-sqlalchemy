from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.db_helper import db_helper
from .utils import authenticate_user, create_access_token
from .token import Token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Token:

    user = await authenticate_user(
        email=form_data.username,
        password=form_data.password,
        session=session,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {
            "sub": user.email,
        },
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
