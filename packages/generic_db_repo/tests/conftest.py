import pytest

from ..dependencies import AsyncSessionLocal, engine, get_async_session  # noqa
from ..generic_db_repository import CRUDBaseRepository  # noqa
from .fixture.fixtures import get_test_session, init_db  # noqa

pytest_mark_anyio = pytest.mark.asyncio
