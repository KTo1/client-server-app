# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового
# представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).

from task_1 import print_info


if __name__ == '__main__':
    words = ['разработка', 'администрирование', 'protocol', 'standard']

    print('To bytes:')
    words = [word.encode(encoding='utf-8') for word in words]
    print_info(words)

    print('To string:')
    words = [word.decode(encoding='utf-8') for word in words]
    print_info(words)



