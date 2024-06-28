import random
import time
import csv
import requests
from bs4 import BeautifulSoup
import json
import datetime
import asyncio
import aiohttp

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


async def get_page_count(session):
    url = 'https://www.labirint.ru/genres/2308/'

    response = await session.get(url=url, headers=headers)

    soup = BeautifulSoup(await response.text(), 'lxml')
    page_count = soup.findAll(
        'div', class_='pagination-number')[-1].text.strip()
    return int(page_count)


async def get_data(session, page):
    global data_books_list

    page_url = f'https://www.labirint.ru/genres/2308/?page={page}'

    async with session.get(url=page_url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

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
                discount_price = edit_number(div_book.find(
                    'span', class_='price-val').text.strip())
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
                price = edit_number(div_book.find(
                    'span', class_='price-old').find('span').text.strip())
                if price == '':
                    price = 'Нет в продаже'
            except Exception:
                price = discount_price

            try:
                discount = edit_number(div_book.find(
                    'span', class_='card-label__text').text.strip())
            except Exception:
                discount = 'Скидки нет'

            async with session.get(url=url, headers=headers) as book_page_response:
                book_page_soup = BeautifulSoup(await book_page_response.text(), 'lxml')

                try:
                    book_available = book_page_soup.find(
                        'div', class_='prodtitle-availibility').find('span').text
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
                'url': url
            }

            data_books_list.append(data_book)

    print(f'Обработал страницу {page}')

    # with open(f'data/{page}_index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)


async def gather_data():  # Формирует список задач
    async with aiohttp.ClientSession() as session:
        page_count = await get_page_count(session)
        print(f'Всего страниц: {page_count}')

        tasks = [asyncio.create_task(get_data(session, page)) for page in range(1, page_count + 1)]

        await asyncio.gather(*tasks)


def main():
    global data_books_list

    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime('%H_%M %d_%m_%y')
    asyncio.run(gather_data())

    with open(f'labirint_{start_time_str}_async.json', 'w', encoding='utf-8') as file:
        json.dump(data_books_list, file, indent=4, ensure_ascii=False)

    with open(f'labirint_{start_time_str}_async.csv', 'w', encoding='cp1251', newline='') as file:
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

    with open(f'labirint_{start_time_str}_async.csv', 'a', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for book in data_books_list:
            writer.writerow(
                (
                    book['book_name'],
                    book['discount_price'],
                    book['old_price'],
                    book['discount'],
                    book['author'],
                    book['publishing_house'],
                    book['book_available'],
                    book['url']
                )
            )

    finish_time = datetime.datetime.now()
    print(f'На выполнение скрипта затрачено {finish_time - start_time}')


if __name__ == '__main__':
    main()