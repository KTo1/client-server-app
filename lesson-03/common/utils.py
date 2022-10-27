import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


def send_message(socket, message):
    """
    Отправляет сообщение через сокет
    """

    if not isinstance(message, dict):
        raise TypeError

    json_string = json.dumps(message)
    message_bytes = json_string.encode(ENCODING)
    socket.send(message_bytes)


def get_message(socket):
    """
    Получает сообщение из сокета, возвращает словарь с информацией о сообщении
    в случае ошибки выбрасывает ValueError
    """

    message_bytes = socket.recv(MAX_PACKAGE_LENGTH)
    if isinstance(message_bytes, bytes):
        json_string = message_bytes.decode(ENCODING)
        if isinstance(json_string, str):
            message = json.loads(json_string)
            if isinstance(message, dict):
                return message

    raise ValueError
