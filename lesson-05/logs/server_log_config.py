import logging


server_log = logging.getLogger('app.main')
formatter = logging.Formatter("<%(asctime)s> <%(levelname)s> <%(module)s> <%(message)s>")

file_hand = logging.FileHandler('server.log', encoding='utf-8')
file_hand.setLevel(logging.DEBUG)
file_hand.setFormatter(formatter)

server_log.addHandler(file_hand)
server_log.setLevel(logging.DEBUG)