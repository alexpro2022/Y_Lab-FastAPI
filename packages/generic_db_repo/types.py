from .generic_db_repository import BaseCRUD, ModelType, Response, _ModelType  # noqa
from typing import TypeAlias, TypeVar


_RepoType = TypeVar('_RepoType', bound=BaseCRUD)
RepoType: TypeAlias = type[_RepoType]
