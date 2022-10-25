# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных
# данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.
# Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
# данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
# в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия
# столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
# столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
# через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().

import re
import csv
import chardet


def get_file_encoding(file_name):
    encoding = 'utf-8'
    with open(file_name, 'rb') as f:
        data = f.read()
        encoding = chardet.detect(data)['encoding']

    return encoding


def append_pattern_data(data, pattern, data_string):
    strings = re.findall(f'{pattern}.*', data_string)
    if strings:
        for string in strings:
            data.append(string.replace(pattern, '').strip())


def get_data():
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for file in files:
        encoding = get_file_encoding(file)
        with open(file, 'r', encoding=encoding) as f:
            data_string = f.read()
            append_pattern_data(os_prod_list, 'Изготовитель ОС:', data_string)
            append_pattern_data(os_name_list, 'Название ОС:', data_string)
            append_pattern_data(os_code_list, 'Код продукта:', data_string)
            append_pattern_data(os_type_list, 'Тип системы:', data_string)

    for idx, data in enumerate(os_prod_list):
        main_data.append([os_prod_list[idx],os_name_list[idx],os_code_list[idx],os_type_list[idx]])

    return main_data


def write_to_csv(file):
    main_data = get_data()
    print(main_data)
    writer = csv.writer(file)
    writer.writerows(main_data)

if __name__ == '__main__':
    file_name = 'main_data.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        write_to_csv(f)