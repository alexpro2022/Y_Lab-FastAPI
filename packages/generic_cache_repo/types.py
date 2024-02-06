from typing import TypeVar

from .generic_cache_repository import BaseRedis

CacheType = TypeVar('CacheType', bound=BaseRedis)
