from app.models import Dish, Menu, Submenu
from app.repositories.db_repository import (CRUDRepository, DishRepository,
                                            MenuRepository, SubmenuRepository)


class TestCRUDRepository:
    @staticmethod
    def test_is_allowed_methods_not_raising_exception() -> None:
        assert CRUDRepository.is_delete_allowed_not_in_use
        assert CRUDRepository.is_update_allowed_not_in_use


class GenericRepoTest:
    def test_repo(self, get_test_session) -> None:
        repo = self.repo(get_test_session)
        assert isinstance(repo, CRUDRepository)
        assert self.model == repo.model
        assert self.msg_not_found == repo.msg_not_found
        assert self.msg_already_exists == repo.msg_already_exists


class TestMenuRepository(GenericRepoTest):
    model = Menu
    repo = MenuRepository
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'


class TestSubmenuRepository(GenericRepoTest):
    model = Submenu
    repo = SubmenuRepository
    msg_not_found = 'submenu not found'
    msg_already_exists = 'Подменю с таким заголовком уже существует.'


class TestDishRepository(GenericRepoTest):
    model = Dish
    repo = DishRepository
    msg_not_found = 'dish not found'
    msg_already_exists = 'Блюдо с таким заголовком уже существует.'
