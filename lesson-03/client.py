import sys
from common.variables import (MAX_CONNECTIONS, DEFAULT_PORT, DEFAULT_IP_ADDRESS)
from common.utils import get_message, send_message, parse_cmd_parameter


def main():
    """
    Запускает клиент.
    Пример: client.py -p 8888 -a 127.0.0.1
    """
    server_address = parse_cmd_parameter('-a', DEFAULT_IP_ADDRESS, 'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    server_port = parse_cmd_parameter('-p', DEFAULT_PORT, 'После параметра -\'p\' необходимо указать номер порта.')

    #process parameter
    try:
        server_port = int(server_port)
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)

