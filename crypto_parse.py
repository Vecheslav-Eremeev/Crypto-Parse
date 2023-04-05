import requests
import datetime
import csv

url = 'https://fapi.binance.com/fapi/v1/klines'  # endpoint для получения котировок
symbols = ['BTCUSDT', 'ETHUSDT']  # выбираем пару ETHUSDT
days_count = 1200

def get_price_change(symbol):
    start_date = int((datetime.datetime.now() - datetime.timedelta(
        days=days_count)).timestamp() * 1000)  # задаем временной интервал - 1 год
    end_date = int(datetime.datetime.now().timestamp() * 1000)

    params = {
        'symbol': symbol,
        'interval': '1d',  # получаем данные по дням
        'startTime': start_date,
        'endTime': end_date,
        'limit': days_count  # максимальное количество строк в ответе - 1000
    }

    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        data = response.json()
        with open(symbol + '_price_change.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Price', 'Price Change'])
            for i in range(len(data)):
                timestamp = datetime.datetime.fromtimestamp(data[i][0] / 1000.0)  # конвертируем timestamp в datetime
                close_price = float(data[i][4])  # получаем цену закрытия
                if i == 0:
                    price_change = 0
                else:
                    price_change = (close_price - float(data[i - 1][4])) / float(
                        data[i - 1][4]) * 100  # изменение цены в процентах
                writer.writerow([timestamp.date(), close_price, f'{price_change:.2f}'])
                print(
                    f'{symbol} futures price on {timestamp.date()}: {close_price:.6f}, price change: {price_change:.2f}%')
    else:
        print(f'Error {response.status_code}: {response.reason}')


def main():
    for symbol in symbols:
        get_price_change(symbol)


if __name__ == '__main__':
    main()
