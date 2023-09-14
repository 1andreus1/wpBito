from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

"""
Путь для хранения статичных файлов
"""

STATIC_PATH = 'static'

YA_CONFIG_FILE = 'ya_config.txt'

TG_CHANNELS_ABS_PATH = path.join(BASE_DIR, STATIC_PATH, YA_CONFIG_FILE)

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