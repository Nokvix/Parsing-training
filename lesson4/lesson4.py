import random
import time
import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

URL = 'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&'
ua = UserAgent()

# def get_persons_url(url):
#     persons_url_list = []
#     for i in range(0, 768, 12):
#         url = f'{url}offset={i}'
#
#         req = requests.get(url).text
#         soup = BeautifulSoup(req, 'lxml')
#
#         persons = soup.find_all('div', class_='bt-slide-content')
#
#         for person in persons:
#             person_url = person.find('a')['href']
#             persons_url_list.append(person_url)
#
#         print('offset =', i)
#
#     with open('persons_url.txt', 'a', encoding='utf-8') as file:
#         for person in persons_url_list:
#             file.write(f'{person}\n')
#
# get_persons_url(URL)

def get_person_data(url):
    ua_random = ua.random
    headers = {
        'user-agent': f'{ua_random}'
    }
    try:
        res = requests.get(url, headers=headers).text
    except Exception:
        print(f'Не получилось собрать данные по ссылке {url}. Пробую снова...')
        time.sleep(random.randrange(2, 4))
        res = get_person_data(url)

    return res


with open('persons_url.txt', 'r', encoding='utf-8') as file:
    urls = [url.strip() for url in file.readlines()]
    data_persons = []

    count = 0
    total_urls = len(urls)
    print(f'Всего итераций: {total_urls}')
    exception_urls = []

    for url in urls:
        # ua_random = ua.random
        # headers = {
        #     'user-agent': f'{ua_random}'
        # }
        # try:
        #     res = requests.get(url, headers=headers).text
        # except Exception:
        #     print(f'Не получилось собрать данные по ссылке {url}. Пробую снова...')
        #     exception_urls.append(url)
        #     time.sleep(random.randrange(2, 4))
        #     res = requests.get(url, headers=headers).text
        res = get_person_data(url)
        soup = BeautifulSoup(res, 'lxml')

        fullname, name_company = soup.find('div', class_='bt-biografie-name').find('h3').text.strip().split(',')
        fullname, name_company = fullname.strip(), name_company.strip()

        social_networks = soup.find('div', class_='bt-profil-kontakt').find_all('a', class_='bt-link-extern')

        social_networks_urls = []
        for item in social_networks:
            social_networks_urls.append(item['href'])

        data = {
            'fullname': fullname,
            'name_company': name_company,
            'social_networks': social_networks_urls
        }

        data_persons.append(data)

        count += 1
        total_urls -= 1
        if total_urls == 0:
            print('Сбор данных закончен!')
        else:
            print(f'#{count}: {url} выполнено! Осталось {total_urls} итераций')
            if count % 12 == 0:
                time.sleep(random.randrange(2, 4))

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_persons, json_file, indent=4, ensure_ascii=False)

    with open('exception_urls.txt', 'w', encoding='utf-8') as exception_file:
        for exc in exception_urls:
            exception_file.write(f'{exc}\n')

