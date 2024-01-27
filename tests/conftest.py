from typing import Any, AsyncGenerator

import pytest

from app.main import app
from packages.generic_db_repo.dependencies import get_async_session
from packages.generic_db_repo.tests.fixture.fixtures import test_session

pytest_plugins = [
    'tests.fixtures.fixtures',
]

pytest_mark_anyio = pytest.mark.asyncio
# pytest_mark_anyio = pytest.mark.anyio


async def override_get_async_session() -> AsyncGenerator[Any, None]:
    async with test_session() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session
