import asyncio

from sqlalchemy.ext.asyncio import AsyncSession


def test_event_loop_fixture(event_loop) -> None:
    event_loop.run_until_complete(asyncio.sleep(0))


def test_get_test_session(get_test_session) -> None:
    assert isinstance(get_test_session, AsyncSession)
