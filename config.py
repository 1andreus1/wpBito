from os import path

ENCODING = 'utf-8'

BASE_DIR = path.dirname(path.abspath(__file__))

"""
Путь для хранения статичных файлов
"""

STATIC_PATH = 'static'

PARAMS_HINTS_FILE = 'params_hints.json'
ACCOUNTS_FILE = 'accounts.json'
PHRASES_FILE = 'phrases.json'
HINTS_FILE = 'hints.json'

PARAMS_HINTS_FILE_ABS_PATH = path.join(BASE_DIR, STATIC_PATH, PARAMS_HINTS_FILE)
ACCOUNTS_FILE_ABS_PATH = path.join(BASE_DIR, STATIC_PATH, ACCOUNTS_FILE)
PHRASES_FILE_ABS_PATH = path.join(BASE_DIR, STATIC_PATH, PHRASES_FILE)
HINTS_FILE_ABS_PATH = path.join(BASE_DIR, STATIC_PATH, HINTS_FILE)

"""
Логи
"""

LOG_FILE = 'logs.log'
LOG_FILES_PATH = 'logs'

LOG_ABS_PATH = path.join(BASE_DIR, LOG_FILES_PATH, LOG_FILE)

'''
Настройки loguru
'''
LOG_FORMAT = '{time} | {level} | {message}'
LOG_ROTATION = '10 MB'

"""
Авторизационные данные для wp.
"""

SITENAME = 'https://normativ24.ru'
PASSWORD = 'OeV4 7Six YOUs t9XV BhwW cnB1'
USER = 'admin'
