from typing import TypeAlias, TypeVar

from .generic_cache_repository import BaseRedis

_CacheType = TypeVar('_CacheType', bound=BaseRedis)
CacheType: TypeAlias = type[_CacheType]
