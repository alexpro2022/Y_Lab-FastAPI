from typing import TypeVar

from .generic_db_repository import BaseCRUD, ModelType  # noqa

RepoType = TypeVar('RepoType', bound=BaseCRUD)
