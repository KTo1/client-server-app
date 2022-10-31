# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в
# файле YAML-формата. Для этого:
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
# третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
# кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
# с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
# ВАЖНО: Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

import yaml


data = {'list': ['1', 2, 3.0, '5'], 'integer': 1, 'dict': {'key1': 'Кей Уан', 'key2': 'key2  €'}}


if __name__ == '__main__':

    file_name = 'yaml_file.yml'
    with open(file_name, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    with open(file_name, 'r', encoding='utf-8') as f:
        data_file = yaml.load(f, Loader=yaml.FullLoader)

    print(f'Данные {"" if str(data) == str(data_file) else "не "}совпадают с исходными.')