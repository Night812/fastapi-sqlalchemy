import asyncio
from datetime import timedelta
import os

import asyncpg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from auth.utils import create_access_token
from core.models import db_helper, PortalRole
from core.config import settings
from main import app

TABLES_FOR_CLEANING = [
    "users",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def run_migrations():
    os.system("alembic init -t async migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(
        url=settings.db.url,
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    yield async_session


@pytest.fixture("")
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in TABLES_FOR_CLEANING:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning}""")


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            url=settings.db.url,
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )
        test_async_session = async_sessionmaker(
            bind=test_engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client():
    """
    Create a new FastAPI TestClient that uses the 'db_session' fixture to override
    the 'get_db' dependency that is injected into routes.
    """

    app.dependency_overrides[db_helper.session_getter] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(
            settings.db.url.split("+asyncpg"),
        ),
    )
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool: asyncpg.Pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM users WHERE user_id = $1;""",
                user_id,
            )

    return get_user_from_database_by_uuid


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        user_id: str,
        name: str,
        surname: str,
        email: str,
        is_active: bool,
        hashed_password: str,
        roles: list[PortalRole],
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                user_id,
                name,
                surname,
                email,
                is_active,
                hashed_password,
                roles,
            )

    return create_user_in_database


def create_test_auth_headers_for_user(email: str) -> dict[str, str]:
    access_token = create_access_token(
        data={
            "sub": email,
        },
        expires_delta=timedelta(
            minutes=settings.auth.access_token_expire_minutes,
        ),
    )
    return {
        "Authorization": f"Bearer {access_token}",
    }
