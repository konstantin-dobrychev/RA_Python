import logging
import sys

from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path
from typing import List


def __logs_directory() -> Path:
    path = Path.home().joinpath('.logs', 'RA_Python')

    if not path.exists():
        path.mkdir(parents=True)

    return path


def __log_file(application: str) -> Path:
    return __logs_directory().joinpath(f'{application}.log')


def __record_format() -> str:
    return '[%(levelname)s] %(asctime)s: %(message)s'


def __datetime_format() -> str:
    return '%d.%m.%Y %H:%M:%S'


def __handlers(application: str) -> List[logging.Handler]:
    return [
        TimedRotatingFileHandler(filename=__log_file(application), when='M', backupCount=3),
        StreamHandler(stream=sys.stdout),
    ]


def configure_logger(application: str):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    for handler in __handlers(application):
        handler.setFormatter(logging.Formatter(__record_format(), __datetime_format()))
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
