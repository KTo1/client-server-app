import sys
import json
import socket

from common.variables import (MAX_CONNECTIONS, RESPONSE, ERROR, TIME, USER, ACTION, ACCOUNT_NAME, PRESENCE,
                              DEFAULT_PORT, DEFAULT_IP_ADDRESS)
from common.utils import get_message, send_message


def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def parse_cmd_parameter(parameter, default_value, error_message):
    try:
        if parameter in sys.argv:
            result = sys.argv[sys.argv.index(parameter) + 1]
        else:
            result = default_value

    except IndexError:
        print(error_message)
        sys.exit(1)

    return result


def main():

    listen_address = parse_cmd_parameter('-a', DEFAULT_IP_ADDRESS, 'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    listen_port = parse_cmd_parameter('-p', DEFAULT_PORT, 'После параметра -\'p\' необходимо указать номер порта.')

    #process parameter
    try:
        listen_port = int(listen_port)
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except ValueError:
        print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    print(f'Сервер запущен по адресу: {listen_address}: {listen_port}')

    while True:
        client_socket, client_address = transport.accept()
        try:
            client_message = get_message(client_socket)
            print(client_message)
            response = process_client_message(client_message)
            send_message(transport, response)

            client_socket.close()

        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента')
            client_socket.close()


if __name__ == '__main__':
    main()
