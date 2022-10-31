# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price),
# покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При
# записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.


import json


def write_order_to_json(item, quantity, price, buyer, date):
    file_name = 'orders.json'
    with open(file_name, 'a+', encoding='utf-8') as f:
        f.seek(0)
        data_string = f.read()
        if data_string:
            data = json.loads(data_string)
        else:
            data = {'orders': []}

        data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    orders = []
    orders.append({'item': 'Товар 1', 'quantity': 1, 'price': 10, 'buyer': 'Покупатель 1', 'date': '01.01.2022'})
    orders.append({'item': 'Товар 2', 'quantity': 2, 'price': 20, 'buyer': 'Покупатель 2', 'date': '02.02.2022'})

    for order in orders:
        write_order_to_json(order['item'], order['quantity'], order['price'], order['buyer'], order['date'])