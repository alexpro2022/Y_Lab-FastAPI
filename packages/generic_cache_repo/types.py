from .generic_cache_repository import BaseRedis
from typing import TypeAlias, TypeVar


_CacheType = TypeVar('_CacheType', bound=BaseRedis)
CacheType: TypeAlias = type[_CacheType]
