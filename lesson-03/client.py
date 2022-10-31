import json
import socket
import sys
import time

from common.variables import (DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, PRESENCE, TIME, USER,
                              ACCOUNT_NAME, RESPONSE, ERROR)
from common.utils import get_message, send_message, parse_cmd_parameter


def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """

    result = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER:{
            ACCOUNT_NAME:account_name
        }
    }

    return result


def process_answer(answer):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''

    if RESPONSE in answer:
        if answer[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {answer[ERROR]}'
    raise ValueError


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

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message = create_presence()
    answer = send_message(transport, message)
    try:
        answer = process_answer(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()