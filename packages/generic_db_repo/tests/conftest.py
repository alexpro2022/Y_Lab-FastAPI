import pytest

from ..dependencies import get_async_session  # noqa
from .fixture.data import *  # noqa
from .fixture.fixtures import *  # noqa

pytest_mark_anyio = pytest.mark.asyncio
