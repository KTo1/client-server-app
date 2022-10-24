# 5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает результат
# из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.

import platform
import subprocess
import chardet


if __name__ == '__main__':
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', '127.0.0.1']
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        encoding = chardet.detect(line)['encoding']
        line = line.decode(encoding).encode('utf-8')
        print(line.decode('utf-8'))