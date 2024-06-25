import json
import time
import random
import requests
from bs4 import BeautifulSoup
import datetime

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    "X-Kl-Ajax-Request": 'Ajax_Request',
    'X-Requested-With': "XMLHttpRequest"
}


def get_json_data():
    url = f'https://roscarservis.ru/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&set_filter=Y&sort%5Brecommendations%5D=asc&limit=16&PAGEN_1=1'

    r = requests.get(url=url, headers=headers)
    json_data = json.loads(r.text)

    with open('json_data.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

    time.sleep(3)


def get_data():
    start_time = datetime.datetime.now()
    get_json_data()

    item_data_list = []

    with open('json_data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    pages_count = json_data['pagesCount']
    print(f'Получил итоговое количество страниц. Их {pages_count}')

    for i in range(1, pages_count + 1):
        print(f'Обрабатываю страницу {i}/{pages_count}...')
        url = f'https://roscarservis.ru/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&set_filter=Y&sort%5Brecommendations%5D=asc&limit=16&PAGEN_1={i}'

        r = requests.get(url=url, headers=headers)
        json_data = r.json()
        items = json_data['items']
        
        number_items = len(items)
        counter = 1

        for item in items:
            name = item['name']
            img_src = f"https://roscarservis.ru{item['imgSrc']}"
            url = item['url']
            price = round(float(item['price']), 2)

            total_count = 0
            info_stores = []
            possible_stores = ['discountStores', 'externalStores', 'commonStores']
            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            amount = int(store['AMOUNT'])
                            total_count += amount
                            price = round(float(store['PRICE']), 2)
                            store_name = store['STORE_NAME']

                            store_data = {
                                'store_name': store_name,
                                'amount': amount,
                                'price': price
                            }

                            info_stores.append(store_data)

            item_data = {
                'name': name,
                'img_src': img_src,
                'url': url,
                'price': price,
                'total_count': total_count,
                'common_stores': info_stores
            }

            item_data_list.append(item_data)
            print(f'Обработан товар {counter}/{number_items}')
            counter += 1

            time.sleep(random.randrange(2, 5))

        print('#' * 20)

    datetime_now = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%y')
    with open(f'{datetime_now}_data.json', 'w', encoding='utf-8') as file:
        json.dump(item_data_list, file)

    diff = datetime.datetime.now() - start_time

    print(f'На сбор данных затрачено: {diff}')


def main():
    get_data()


if __name__ == '__main__':
    main()
