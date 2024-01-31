import re

from fastapi import status


def get_regex(expected_msg: str, expected_error_code: int | None = None) -> str:
    error_code = '' if expected_error_code is None else f'{expected_error_code}: '
    return re.escape(f'{error_code}{expected_msg}')


def get_regex_not_found(msg_not_found: str) -> str:
    return get_regex(msg_not_found, status.HTTP_404_NOT_FOUND)
