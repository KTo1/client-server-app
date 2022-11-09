import sys
import json
import time
import socket

from common.variables import (DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, PRESENCE, TIME, USER,
                              ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_MODE, DEFAULT_USER, MESSAGE, EXIT)
from common.utils import get_message, send_message, parse_cmd_parameter
from logs.client_log_config import client_log
from logs.decorators import log


@log
def create_presence(account_name):
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


@log
def create_exit_message(account_name):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """

    result = {
        ACTION: EXIT,
        TIME: time.time(),
        USER:{
            ACCOUNT_NAME:account_name
        }
    }

    return result

@log
def create_message(message, account_name):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """

    result = {
        ACTION: MESSAGE,
        TIME: time.time(),
        MESSAGE: message,
        USER:{
            ACCOUNT_NAME:account_name
        }
    }

    return result


@log
def process_answer(answer):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''

    if RESPONSE in answer:
        if answer[RESPONSE] == 200:
            return '200 : OK'

        if answer[RESPONSE] == 201:
            time_string = time.strftime('%d.%m.%Y %H:%M', time.localtime(answer[TIME]))
            return f'<{time_string}> {answer[USER]}: {answer[MESSAGE]}'

        if answer[RESPONSE] == 202:
            time_string = time.strftime('%d.%m.%Y %H:%M', time.localtime(answer[TIME]))
            return f'<{time_string}> {answer[USER]}: {answer[MESSAGE]}'

        return f'400 : {answer[ERROR]}'

    raise ValueError


def main():
    """
    Запускает клиент.
    -m send - для отправки сообщений
    -m get - общий чат, где будут приниматься сообщения
    -u User - имя пользователя
    Пример: client.py -m send -u Guest -p 8888 -a 127.0.0.1
    Пример: client.py -m get -u Guest -p 8888 -a 127.0.0.1
    """

    server_address = parse_cmd_parameter('-a', sys.argv, DEFAULT_IP_ADDRESS, 'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    server_port = parse_cmd_parameter('-p', sys.argv, DEFAULT_PORT, 'После параметра -\'p\' необходимо указать номер порта.')
    run_mode = parse_cmd_parameter('-m', sys.argv, DEFAULT_MODE, 'После параметра -\'m\' необходимо указать режим запуска.')
    user_name = parse_cmd_parameter('-u', sys.argv, DEFAULT_USER, 'После параметра -\'m\' необходимо указать имя пользователя.')

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

    message = create_presence(user_name)
    send_message(transport, message)

    try:
        answer = process_answer(get_message(transport))
        print(answer)

    except (ValueError, json.JSONDecodeError):
        client_log.exception('Не удалось декодировать сообщение сервера.')
        sys.exit(1)

    if answer == '200':
        pass

    if run_mode == 'send':
        while True:
            msg = input(f'<{user_name}> Введите непустое сообщение (exit для выхода): ')
            if not msg:
                continue

            if msg == 'exit':
                send_message(transport, create_exit_message(user_name))
                time.sleep(3)
                break

            send_message(transport, create_message(msg, user_name))

    if run_mode == 'get':
        while True:
            answer = process_answer(get_message(transport))
            print(answer)


if __name__ == '__main__':
    main()