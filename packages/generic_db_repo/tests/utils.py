from fastapi import status


def check_exception_info(exc_info, expected_msg: str, expected_error_code: int | None = None) -> None:
    assert expected_msg in exc_info.value.args
    if expected_error_code is not None:
        assert expected_error_code in exc_info.value.args


def check_exception_info_not_found(exc_info, msg_not_found: str) -> None:
    check_exception_info(exc_info, msg_not_found, status.HTTP_404_NOT_FOUND)
