# 2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в
# автоматическом, а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в
# коем случае не используя методы encode, decode или функцию bytes) и определить тип, содержимое и длину
# соответствующих переменных.


def str_to_byte(string):
    return eval(f"b'{string}'")


if __name__ == '__main__':
    words = ['class', 'function', 'method']
    for word in words:
        word_b = str_to_byte(word)
        print(f'''Type of '{word_b}' id {type(word_b)}. Length = {len(word_b)}''')

