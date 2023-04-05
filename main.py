last_price = None

import requests
import time

# Параметры для подключения к API
symbol = 'ETHUSDT'
interval = '1m'


def main():
    # Бесконечный цикл считывания данных и определения изменения цен
    while True:
        # Получение данных о цене фьючерса с Binance API
        r = requests.get(f'https://fapi.binance.com/fapi/v1/ticker/24hr?symbol={symbol}')
        data = r.json()
        price = float(data['lastPrice'])

        # Запись текущей цены в файл
        with open('price_history.txt', 'a') as f:
            now = int(time.time())
            f.write(f'{now},{price}\n')

        # Вычисление изменения цены за последние 60 минут
        past_price = None
        with open('price_history.txt', 'r') as f:
            for line in f:
                ts, past_price = line.strip().split(',')
                if int(time.time()) - int(ts) >= 60 * 60:  # Находим последнюю цену для расчета изменения цены на 1%
                    break

        if past_price:
            change = (price - float(past_price)) / float(past_price) * 100
            if abs(change) >= 1:
                print(f'Цена {symbol} изменилась на {change:.2f}% за последний час')

        time.sleep(60)  # Ждем 1 минуту перед получением новых данных


if __name__ == '__main__':
    main()


