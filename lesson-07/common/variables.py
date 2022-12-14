""" Константы """

# Порт по умолчанию для сетевого взаимодействия
DEFAULT_PORT = 8888
# IP адрес по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'
# режим запуска по умолчанию
DEFAULT_MODE = 'send'
# имя пользователя по умолчанию
DEFAULT_USER = 'Guest'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 4096
# Кодировка проекта
ENCODING = 'utf-8'

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
MESSAGE = 'message'
RESPONSE = 'response'
ERROR = 'error'
EXIT = 'exit'