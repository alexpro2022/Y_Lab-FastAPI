from typing import TypeVar

from .generic_db_repository import BaseCRUD, ModelType, Response  # noqa

RepoType = TypeVar('RepoType', bound=BaseCRUD)
