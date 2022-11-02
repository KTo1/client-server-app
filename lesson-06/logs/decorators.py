import os
import sys

from client_log_config import client_log
from server_log_config import server_log


def log(func):

    dirpath, file_name = os.path.split(sys.argv[0])
    logger = client_log if file_name == 'client.py' else server_log

    def wrapper(*args, **kwargs):
        logger.debug(func.__name__)
        result = func(*args, **kwargs)
        return result
    return wrapper