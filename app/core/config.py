import re

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str
    port: int
    reload: bool = True


class Security(BaseModel):
    access_token_expire_minutes: int = 30
    secret_key: str = "secret_key"
    algorithm: str = "HS256"


class Database(BaseModel):
    url: str
    echo: bool
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        case_sensitive=False,
    )

    run: RunConfig
    db: Database
    auth: Security = Security()


settings = Settings()
LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
