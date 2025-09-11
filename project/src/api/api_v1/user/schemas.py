import uuid

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from src.core.config import LETTER_MATCH_PATTERN


class TunedModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class ShowUser(TunedModel):
    user_id: uuid.UUID
    email: EmailStr
    name: str
    surname: str
    is_active: bool
    roles: list


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str

    @field_validator("name")
    def validate_name(cls, value: str):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value: str):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return value


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None
    surname: str | None = None

    @field_validator("name")
    def validate_name(cls, value: str | None):

        if value is None:
            return None

        elif not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return value

    @field_validator("surname")
    def validate_surname(cls, value: str | None):

        if value is None:
            return None

        elif not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return value
