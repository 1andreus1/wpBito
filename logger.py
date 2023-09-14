from loguru import logger as log

from config import (
    LOG_ABS_PATH,
    LOG_FORMAT,
    LOG_ROTATION
)

log.add(
    LOG_ABS_PATH,
    format=LOG_FORMAT,
    rotation=LOG_ROTATION,
    compression='zip'
)

if __name__ == '__main__':
    """from logger import log"""
    log.info('Тестовый лог')
