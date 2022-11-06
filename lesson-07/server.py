import sys
import json
import socket

from select import select

from common.variables import (MAX_CONNECTIONS, RESPONSE, ERROR, TIME, USER, ACTION, ACCOUNT_NAME, PRESENCE,
                              DEFAULT_PORT, DEFAULT_IP_ADDRESS, MESSAGE)
from common.utils import get_message, send_message, parse_cmd_parameter
from logs.server_log_config import server_log
from logs.decorators import log


USERS = ['Guest', 'Bazil', 'KTo', 'User']


@log
def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента
    """

    server_log.debug(f'Вызов функции "process_client_message", с параметрами: {str(message)}')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] in USERS:
        return {RESPONSE: 200}

    if ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] in USERS:
        return {RESPONSE: 201, MESSAGE: message}

    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Запускает сервер.
    Пример: server.py -p 8888 -a 127.0.0.1
    """

    listen_address = parse_cmd_parameter('-a', sys.argv, DEFAULT_IP_ADDRESS, 'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    listen_port = parse_cmd_parameter('-p', sys.argv, DEFAULT_PORT, 'После параметра -\'p\' необходимо указать номер порта.')

    if listen_port is None or listen_address is None:
        server_log.error('Неверно заданы параметры командной строки')
        sys.exit(1)

    #process parameter
    try:
        listen_port = int(listen_port)
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except ValueError:
        server_log.exception('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)
    transport.settimeout(1)

    clients_sockets = []
    server_log.info(f'Сервер запущен по адресу: {listen_address}: {listen_port}')

    while True:
        try:
            client_sock, client_address = transport.accept()
        except OSError as e:
            print(str(e))
        else:
            clients_sockets.append(client_sock)
        finally:
            wait = 0
            message_pool = []

            for client_socket in clients_sockets:
                # На мой взгляд логичнее это вынести за цикл, но на виндовс так не работает
                cl_sock_read, cl_sock_write, _ = select(clients_sockets, clients_sockets, [], wait)
                try:
                    if client_socket in cl_sock_read:
                        client_message = get_message(client_socket)
                        print(client_message)
                        response = process_client_message(client_message)

                        # Пока так, 200 это приветствие
                        if response[RESPONSE] == 200 and client_socket in cl_sock_write:
                            send_message(client_socket, response)

                        # Пока так, 201 это сообщение всем
                        if response[RESPONSE] == 201:
                            message_pool.append(response[MESSAGE])

                except (ValueError, json.JSONDecodeError):
                    server_log.exception('Принято некорректное сообщение от клиента')
                    clients_sockets.remove(client_socket)
                    client_socket.close()

            for message in message_pool:
                for client_socket in clients_sockets:
                    _, cl_sock_write, _ = select(_, clients_sockets, [], wait)
                    if client_socket in cl_sock_write:
                        pass


if __name__ == '__main__':
    main()
