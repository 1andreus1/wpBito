import json

from config import ENCODING


def load_json_file(path: str) -> dict:
    """
    :param path: Путь до .json файла.
    """
    with open(path, 'r', encoding=ENCODING) as file:
        json_data = json.load(file)
    return json_data
