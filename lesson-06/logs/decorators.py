import os
import sys

from client_log_config import client_log
from server_log_config import server_log


def log(func):

    dir_path, file_name = os.path.split(sys.argv[0])
    loggi = client_log if file_name == 'client.py' else server_log

    def wrapper(*args, **kwargs):
        loggi.debug(func.__name__)
        result = func(*args, **kwargs)
        return result
    return wrapper