import json

from config import (
    ENCODING,
    PARAMS_HINTS_FILE_ABS_PATH,
    ACCOUNTS_FILE_ABS_PATH,
    PHRASES_FILE_ABS_PATH, HINTS_FILE_ABS_PATH,
)
from src.utils.utils import load_json_file


def load_hints_params() -> dict:
    """
    Загружает параметры запроса для получения подсказок.

    :return: (dict) параметры запроса.
    """
    return load_json_file(
        PARAMS_HINTS_FILE_ABS_PATH
    )


def load_accounts() -> list:
    json_data = load_json_file(
        ACCOUNTS_FILE_ABS_PATH
    )

    return [
        list(account.values()) for account in json_data.values()
    ]


def load_phrases() -> dict:
    phrases = load_json_file(
        PHRASES_FILE_ABS_PATH
    )
    return phrases


def load_hints() -> dict:
    hints = load_json_file(
        HINTS_FILE_ABS_PATH
    )
    return hints


def save_hints(hints, append_mode: bool = True):
    file_mode = "w+" if append_mode else "w"

    with open(
            HINTS_FILE_ABS_PATH,
            mode=file_mode,
            encoding=ENCODING
    ) as file:
        json.dump(
            hints,
            file,
            ensure_ascii=False,
            sort_keys=False,
            indent=4,
            separators=(',', ': ')
        )
