import random
import time
import csv
import requests
from bs4 import BeautifulSoup
import json
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    'Accept': '*/*'
}

data_books_list = []


def edit_number(discount_str: str):
    discount = ''
    for char in discount_str:
        if char.isdigit():
            discount += char

    return discount





def get_page_count():
    url = 'https://www.labirint.ru/genres/2308/'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    page_count = soup.findAll('div', class_='pagination-number')[-1].text.strip()
    return int(page_count)


def get_page(i):
    url = f'https://www.labirint.ru/genres/2308/?page={i}'

    r = requests.get(url=url, headers=headers)

    with open(f'data/{i}_index.html', 'w', encoding='utf-8') as file:
        file.write(r.text)


def get_data(i):
    global data_books_list

    with open(f'data/{i}_index.html', 'r', encoding='utf-8') as file:
        page = file.read()

    soup = BeautifulSoup(page, 'lxml')

    book_cards = soup.findAll('div', class_='genres-carousel__item')

    counter = 1
    for book in book_cards:
        div_book = book.find('div')
        book_id = div_book['data-product-id']
        url = f'https://www.labirint.ru/books/{book_id}/'

        try:
            book_name = div_book['data-name']
        except Exception:
            book_name = 'Нет названия книги'

        try:
            discount_price = edit_number(div_book.find('span', class_='price-val').text.strip())
            if discount_price == '':
                discount_price = 'Нет в продаже'
        except Exception:
            discount_price = 'Нет в продаже'

        try:
            pubhouse = div_book['data-pubhouse']
        except Exception:
            pubhouse = 'Нет данных об издательстве'

        try:
            author = div_book.find('div', class_='product-author').text.strip()
        except Exception:
            author = 'Нет данных об авторе'

        try:
            price = edit_number(div_book.find('span', class_='price-old').find('span').text.strip())
            if price == '':
                price = 'Нет в продаже'
        except Exception:
            price = discount_price

        try:
            discount = edit_number(div_book.find('span', class_='card-label__text').text.strip())
        except Exception:
            discount = 'Скидки нет'

        book_page = requests.get(url=f'https://www.labirint.ru/books/{book_id}/', headers=headers).text
        book_page_soup = BeautifulSoup(book_page, 'lxml')

        try:
            book_available = book_page_soup.find('div', class_='prodtitle-availibility').find('span').text
        except Exception:
            book_available = 'Не данных о наличии книги'

        data_book = {
            'book_name': book_name,
            'discount_price': discount_price,
            'old_price': price,
            'discount': discount,
            'author': author,
            'publishing_house': pubhouse,
            'book_available': book_available,
            'url': f'https://www.labirint.ru/books/{book_id}/'
        }

        with open('data.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    book_name,
                    discount_price,
                    price,
                    discount,
                    author,
                    pubhouse,
                    book_available,
                    url
                )
            )

        data_books_list.append(data_book)
        print(f'Обработал данные книги {counter}/{len(book_cards)}')
        counter += 1

def main():
    global data_books_list

    start_time = datetime.datetime.now()
    page_count = get_page_count()
    print(f'Всего страниц на сайте: {page_count}')

    with open('data.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                "Название книги",
                "Цена со скидкой",
                "Цена без скидки",
                "Скидка %",
                "Автор",
                "Издательство",
                "Наличие",
                "Ссылка"
            )
        )

    for i in range(1, page_count + 1):
        print('#' * 20)
        print(f'Собираю данные со страницы {i}/{page_count}')
        get_page(i)
        get_data(i)
        time.sleep(random.randrange(2, 4))

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data_books_list, file, indent=4, ensure_ascii=False)



    diff = datetime.datetime.now() - start_time
    print(f'Затрачено на парсинг {diff}')


if __name__ == '__main__':
    main()
