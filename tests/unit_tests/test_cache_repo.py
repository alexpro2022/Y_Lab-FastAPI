from packages.generic_cache_repo.testing_tools.testing_lib import BaseRedisTest
from tests.fixtures.data import CREATE_PAYLOAD, Model


class TestBaseRedis(BaseRedisTest):
    model = Model
    create_data = CREATE_PAYLOAD
