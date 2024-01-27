from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (CRUDRepository, DishRepository,
                                            MenuRepository, SubmenuRepository)


class TestCRUDRepository:
    @staticmethod
    def test_is_allowed_methods_not_raising_exception() -> None:
        assert CRUDRepository.is_delete_allowed_not_in_use
        assert CRUDRepository.is_update_allowed_not_in_use


def generic_test_repo(_self, repo, session, model) -> None:
    repo = repo(session)
    assert isinstance(repo, CRUDRepository)
    assert repo.model == model, (repo.model, model)
    assert _self.msg_not_found == repo.msg_not_found
    assert _self.msg_already_exists == repo.msg_already_exists


class TestMenuRepository:
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'

    def test_repo(self, get_test_session: AsyncSession) -> None:
        generic_test_repo(self, MenuRepository, get_test_session, Menu)


class TestSubmenuRepository:
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'

    def test_repo(self, get_test_session: AsyncSession) -> None:
        generic_test_repo(self, SubmenuRepository, get_test_session, Submenu)


class TestDishRepository:
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'

    def test_repo(self, get_test_session: AsyncSession) -> None:
        generic_test_repo(self, DishRepository, get_test_session, Dish)
