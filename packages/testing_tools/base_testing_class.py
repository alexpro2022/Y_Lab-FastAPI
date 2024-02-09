import re
from fastapi import status
from typing import Any
from deepdiff import DeepDiff


class BaseTestingClass:
    msg_already_exists: str = 'Object with such a unique values already exists.'
    msg_not_found: str = 'Object(s) not found.'
    create_data: dict
    create_data_extra: dict
    update_data: dict

# --- Utils ---
    @staticmethod
    def get_regex(expected_msg: str, expected_error_code: int | None = None) -> str:
        error_code = '' if expected_error_code is None else f'{expected_error_code}: '
        return re.escape(f'{error_code}{expected_msg}')

    def get_regex_already_exists(self) -> str:
        return self.get_regex(self.msg_already_exists, status.HTTP_400_BAD_REQUEST)

    def get_regex_not_found(self) -> str:
        return self.get_regex(self.msg_not_found, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def compare_obj_data(obj, data: dict) -> None:
        for key in data:
            assert getattr(obj, key) == data[key]

    @staticmethod
    def compare_objs(left: Any, right: Any) -> None:
        assert isinstance(left, type(right)), (type(left), type(right))
        diff = DeepDiff(left, right, exclude_paths='_sa_instance_state')
        assert not diff, diff

    def compare_lists(self, left: list | None, right: list | None) -> None:
        assert left and isinstance(left, list)
        assert right and isinstance(right, list)
        assert len(left) == len(right)
        for i in range(len(left)):
            self.compare_objs(left[i], right[i])

    @staticmethod
    async def _is_empty(repo) -> bool:
        res = await repo.get()
        return res is None or res == []
