# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
# «декоратор». Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед
# нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в
# какой кодировке он был создан.

from chardet import detect


if __name__ == '__main__':
    file_name = 'test_file.txt'
    words = ['сетевое программирование', 'сокет', 'декоратор']
    with open(file_name, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

    with open(file_name, 'rb') as f:
        data = f.read()
    encoding = detect(data)['encoding']
    print('encoding: ', encoding)

    with open(file_name, encoding=encoding) as f:
        print(f.read())

