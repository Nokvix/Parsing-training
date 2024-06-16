import csv
import json
import random
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

MAX_VAL = 140
STEP = 20
ua = UserAgent()


def get_data(url):
    for i in range(0, MAX_VAL + 1, STEP):
        url = f'https://www.tury.ru/hotel/?cn=0&ct=0&cat=1317&txt_geo=&srch=&s={i}'

        headers = {
            'User-Agent': ua.random,
        }

        r = requests.get(url, headers=headers).text

        with open(f'data/{i}_index.html', 'w', encoding='utf-8') as file:
            file.write(r)

        soup = BeautifulSoup(r, 'lxml')
        hotel_urls = soup.find_all('div', class_='reviews-travel__item')

        with open(f'data/{i}_hotel_urls.txt', 'w', encoding='utf-8') as file:
            for hotel_url in hotel_urls:
                link = hotel_url.find('a', class_='reviews-travel__title title flex')['href']
                file.write(f'{link}\n')
        print(f'Итерация {i} из {MAX_VAL}')
        time.sleep(random.randrange(2, 4))


def get_hotel_data():
    hotels_list = []
    for i in range(0, MAX_VAL + 1, STEP):
        with open(f'data/{i}_hotel_urls.txt', 'r', encoding='utf-8') as file:
            urls = [url.replace('\n', '') for url in file.readlines()]
            counter = 1 + i
            for url in urls:
                headers = {
                    'User-Agent': ua.random,
                }

                r = requests.get(url, headers=headers).text
                soup = BeautifulSoup(r, 'lxml')

                hotel_name = soup.find('div', class_='h1').text.strip()[:-3]
                number_of_stars = soup.find('div', class_='h1').text.strip()[-3:]
                hotel_description = soup.find('div', class_='hotel__text').text.strip()
                hotel_location = soup.find('div', class_='hotel-contact__item').find('a').text.strip()

                hotel_data = {
                    'hotel_name': hotel_name,
                    'number_of_stars': number_of_stars,
                    'hotel_description': hotel_description,
                    'hotel_location': hotel_location,
                    'url': url
                }
                hotels_list.append(hotel_data)
                print(f'Записан {counter}-й отель')
                counter += 1
            time.sleep(random.randrange(2, 4))

    with open('hotel_data.json', 'w', encoding='utf-8') as file:
        json.dump(hotels_list, file, indent=4, ensure_ascii=False)
        add_to_csv(hotels_list)


def add_to_csv(hotels_list):
    with open('hotels_data.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                'Название',
                'Количество звёзд отеля',
                'Описание отеля',
                'Андрес отеля',
                'Ссылка'
            )
        )

    for hotel in hotels_list:
        with open('hotels_data.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    hotel['hotel_name'],
                    hotel['number_of_stars'],
                    hotel['hotel_description'],
                    hotel['hotel_location'],
                    hotel['url']
                )
            )


def main():
    url = 'https://www.tury.ru/hotel/most_luxe.php'
    get_data(url)
    get_hotel_data()


if __name__ == '__main__':
    main()
