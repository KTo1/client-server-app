# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
# Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.


from task_2 import str_to_byte


def can_convert(string):
    try:
        str_to_byte(string)
        return True
    except:
        return False


if __name__ == '__main__':
    words = ['attribute', 'класс', 'функция', 'type']
    for word in words:
        print(f'''Word '{word}' can{"" if can_convert(word) else "'t"} convert to byte''')