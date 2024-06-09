import json
import random
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent


def requests_get(url):
    ua_random = ua.random
    headers = {
        'user-agent': f'{ua_random}'
    }
    req = requests.get(url, headers=headers)
    return req


def get_festival_urls():
    festival_urls = []
    for i in range(0, 289, 24):

        url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=9%20Jun%202024&to_date=&maxprice=500&o={i}&bannertitle=June'
        req = requests_get(url)
        json_data = json.loads(req.text)
        html_response = json_data['html']
        with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
            file.write(html_response)

        with open(f'data/index_{i}.html', 'r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        links = soup.find_all('a', class_='card-img-link')
        for link in links:
            cur_link = 'https://www.skiddle.com' + link['href']
            festival_urls.append(cur_link)

    with open('festival_urls.txt', 'a', encoding='utf-8') as file:
        for link in festival_urls:
            file.write(f'{link}\n')


fest_data_list = []


def get_festival_data():
    with open('festival_urls.txt', 'r', encoding='utf-8') as file:
        festival_urls = [link.strip() for link in file.readlines()]

    NULL_STRING = 'Be the first to leave a review!'
    counter = 0
    total_fests = len(festival_urls)
    print(f'Всего {total_fests} итераций')
    for url in festival_urls:
        req = requests_get(url)

        try:
            soup = BeautifulSoup(req.text, 'lxml')
            festival_name = soup.find('h1', class_='MuiTypography-root MuiTypography-body1 css-159aw2y').text.strip()
            festival_date_and_location = soup.find_all('div',
                                                       class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')[
                                         :2]
            festival_date = festival_date_and_location[0].text.strip()
            festival_location = festival_date_and_location[1].text.strip()
            festival_description = soup.find('p').text.strip()

            fest_data_list.append({
                'Название фестиваля': festival_name,
                'Сроки проведения фестиваля ': festival_date,
                'Место проведения': festival_location,
                'О фестивале': festival_description if festival_description != NULL_STRING else 'Текстовой информации о фестивале нет',
                'Ссылка': url
            })

        except Exception as ex:
            print(ex)
            print('Упс... Случилась какая-то ошибка... Пробую снова')
        counter += 1
        total_fests -= 1
        print(f'Итерация #{counter} {url} выполнено! Осталось {total_fests} итераций')
        if counter % 24 == 0:
            time.sleep(random.randrange(2, 4))


# get_festival_urls()
get_festival_data()

with open('fest_data.json', 'a', encoding='utf-8') as file:
    json.dump(fest_data_list, file, indent=4, ensure_ascii=False)
