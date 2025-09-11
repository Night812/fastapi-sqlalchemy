import asyncio
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from project.src.core.models.base import Base
from project.src.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        url=settings.db_testing.url,
        echo=settings.db_testing.echo,
        echo_pool=settings.db_testing.echo_pool,
        pool_size=settings.db_testing.pool_size,
        max_overflow=settings.db_testing.max_overflow,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop tables

    await engine.dispose()
