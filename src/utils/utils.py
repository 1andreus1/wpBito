import time
from enum import Enum
from typing import Any

import requests
import urllib3

from new_project.exceptions import TooManyRequestsError, BadStatusCodeError

MAX_RETRIES = 6
ENCODING = 'utf-8'

ERRORS_FOR_RETRY = (
    TooManyRequestsError,
    ConnectionError,
    BadStatusCodeError,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def wait_for_response(func) -> Any:
    def wrapper(*args, **kwargs) -> Any:
        delay = 1

        for _ in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except ERRORS_FOR_RETRY:
                print(delay)
                time.sleep(delay)
                delay *= 2

        return func(*args, **kwargs)

    return wrapper


class HTTPMethod(Enum):
    GET = requests.get
    POST = requests.post


class DecodeTo(Enum):
    CONTENT: object = lambda res: res.content
    TEXT: object = lambda res: res.text
    JSON: object = lambda res: res.json()


@wait_for_response
def get_url(method, decoder, url, **kwargs):
    print(url)
    res = method(url, **kwargs)
    print(res.json())
    res.encoding = ENCODING
    check_status_code(res.status_code)
    return decoder(res)


def check_status_code(status_code: int) -> None:
    if 199 < status_code < 300:
        return

    if status_code == 503:
        raise TooManyRequestsError
    else:
        print(f'Статус {status_code}')
        raise BadStatusCodeError(f'Статус {status_code}')


def get_file_content(url: str) -> bytes:
    content = get_url(
        HTTPMethod.GET,
        DecodeTo.CONTENT,
        url,
    )
    return content
