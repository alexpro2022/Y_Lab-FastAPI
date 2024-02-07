from app.repositories.cache_repository import MenuCache
from app.repositories.db_repository import MenuCRUD
from packages.generic_service_repo.generic_service_repository import BaseService
from packages.generic_service_repo.testing_tools.testing_lib import BaseServiceTest
from tests.fixtures import data as d


class TestBaseServicewithMenu(BaseServiceTest):
    service = BaseService
    db = MenuCRUD
    cache = MenuCache
    msg_not_found = 'menu not found'
    msg_already_exists = 'Меню с таким заголовком уже существует.'
    create_data = d.MENU_POST_PAYLOAD
    update_data = d.MENU_PATCH_PAYLOAD
