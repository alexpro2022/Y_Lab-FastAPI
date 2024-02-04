from packages.generic_cache_repo.dependencies import redis
from packages.generic_cache_repo.generic_cache_repository import BaseRedis


class MenuCache(BaseRedis):

    def __init__(self, redis: redis, redis_expire: int = 3600):
        super().__init__(redis, 'menu:', redis_expire)


class SubmenuCache(BaseRedis):

    def __init__(self, redis: redis, redis_expire: int = 3600):
        super().__init__(redis, 'submenu:', redis_expire)


class DishCache(BaseRedis):

    def __init__(self, redis: redis, redis_expire: int = 3600):
        super().__init__(redis, 'dish:', redis_expire)
