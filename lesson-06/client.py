import json
import socket
import sys
import time

from common.variables import (DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, PRESENCE, TIME, USER,
                              ACCOUNT_NAME, RESPONSE, ERROR)
from common.utils import get_message, send_message, parse_cmd_parameter
from logs.client_log_config import client_log


def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """

    client_log.debug(f'Вызов функции "create_presence", с параметрами: {str(account_name)}')

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

    client_log.debug(f'Вызов функции "process_answer", с параметрами: {str(answer)}')

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

    server_address = parse_cmd_parameter('-a', sys.argv, DEFAULT_IP_ADDRESS, 'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    server_port = parse_cmd_parameter('-p', sys.argv, DEFAULT_PORT, 'После параметра -\'p\' необходимо указать номер порта.')

    if server_port is None or server_address is None:
        client_log.error('Неверно заданы параметры командной строки')
        sys.exit(1)

    #process parameter
    try:
        server_port = int(server_port)
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        client_log.exception('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        transport.connect((server_address, server_port))
    except ConnectionRefusedError as e:
        client_log.exception(str(e))
        sys.exit(1)

    message = create_presence()
    send_message(transport, message)

    try:
        answer = process_answer(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        client_log.exception('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()