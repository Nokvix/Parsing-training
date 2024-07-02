import json
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from fake_useragent import FakeUserAgent
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import asyncio
import aiohttp

ua = FakeUserAgent()
items_list = []


def create_headers():
    headers = {
        'User-Agent': f'{ua.random}',
        'Accept': '*/*'
    }

    return headers


def get_html_code(url):
    print('Получаю html код для последующей его обработки')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--proxy-server=91.195.125.167:8000')
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(url=url)
        driver.implicitly_wait(3)

        counter = 0
        while not driver.find_elements(By.CLASS_NAME, 'service-items-medium'):
            time.sleep(1)
            counter += 1
            if counter == 60:
                raise Exception

        while True:

            if not driver.find_elements(By.CLASS_NAME, 'reset-filters-btn'):
                block_button_show_more = driver.find_element(By.CLASS_NAME, 'catalog-button-showMore')
                button_show_more = driver.find_element(By.CLASS_NAME, 'button-show-more')
                # driver.execute_script('arguments[0].scrollIntoView(true)', button_show_more)  # С помощью javascript
                ActionChains(driver).scroll_to_element(block_button_show_more).click(button_show_more).perform()

                driver.implicitly_wait(3)
            else:
                block_button_show_more = driver.find_element(By.CLASS_NAME, 'catalog-button-showMore')
                ActionChains(driver).scroll_to_element(block_button_show_more).perform()
                driver.implicitly_wait(3)

                with open('async_code/page.html', 'w', encoding='utf-8') as file:
                    file.write(driver.page_source)

                break

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    print('Получил html код страницы')
    print("#" * 30)


def get_items_urls(file_path):
    print('Начинаю сбор ссылок')
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')

    items = soup.find('ul', class_='service-items-medium').find_all('li', class_='minicard-item')

    with open('async_code/items_urls.txt', 'w', encoding='utf-8') as file:
        for item in items:
            item_url = item.find('div', class_='minicard-item__title').find('a', class_='title-link')['href']
            file.write(f'{item_url}\n')

    print('Ссылки собраны')
    print('#' * 30)


def get_correct_url(url):
    return unquote(url).split('?to=')[1].split('&')[0]


async def get_response(session, url, retry=3):
    try:
        async with session.get(url=url, headers=create_headers()) as response:
            return await response.text()
    except Exception as ex:
        if retry == 0:
            print(ex)
            raise Exception
        else:
            print(f'retry -> {retry}')
            await asyncio.sleep(4)
            return await get_response(session, url, retry=(retry - 1))


async def get_item_data(session, url, urls_count):
    try:
        response = await get_response(session, url)
        soup = BeautifulSoup(response, 'lxml')
    except Exception as ex:
        print(f'Ошибка с ссылкой: {url}')
        return

    try:
        title = soup.find('span', {'itemprop': 'name'}).text.strip()
    except Exception as ex:
        title = None

    try:
        phone_numbers = [number['href'].split(':')[-1] for number in
                         soup.find('div', class_='service-phones-list').find_all('a')]
    except Exception as ex:
        phone_numbers = None

    try:
        city_address = soup.find('meta', {'itemprop': 'addressLocality'})['content']
        street_address = soup.find('meta', {'itemprop': 'streetAddress'})['content']
        address = f'{city_address}, {street_address}'
    except Exception as ex:
        address = None

    try:
        website = soup.find('div', class_='service-website-value').find('a').text.strip()
    except Exception as ex:
        website = None

    try:
        social_networks_html_list = soup.find('div', {'data-uitest': 'org-social-list'}).find_all('a')
        social_networks = {}
        for network in social_networks_html_list:
            social_networks[network['data-type']] = get_correct_url(network['href'])
    except Exception as ex:
        social_networks = None

    items_list.append(
        {
            'title': title,
            'url': url,
            'address': address,
            'phone_numbers': phone_numbers,
            'website': website,
            'social_networks': social_networks
        }
    )

    print(f'Обработал страницу клиники: {title}\n'
          f'Прогресс сбора: {len(items_list)}/{urls_count}')
    await asyncio.sleep(random.randrange(3, 5))

    # if len(items_list) % 10 == 0:
    #     time.sleep(random.randrange(3, 5))


async def gather_data(file_path):
    global items_list

    print('Начинаю сбор данных')
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [url.strip() for url in file.readlines()]

    urls_count = len(urls)

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_item_data(session, url, urls_count)) for url in urls]

        await asyncio.gather(*tasks)

    with open('async_code/items.json', 'w', encoding='utf-8') as file:
        json.dump(items_list, file, indent=4, ensure_ascii=False)


def main():
    start_time = datetime.datetime.now()

    # get_html_code(url='https://zoon.ru/spb/medical/type/detskaya_poliklinika/page-1/')
    time_after_receipt_html = datetime.datetime.now()
    print(f'[TIME INFO] На получение html страницы понадобилось {time_after_receipt_html - start_time}')

    # get_items_urls(r'D:\Обучение парсингу\Parsing-training\lesson11\async_code\page.html')
    time_after_receipt_urls = datetime.datetime.now()
    print(f'[TIME INFO] На сбор ссылок понадобилось {time_after_receipt_urls - time_after_receipt_html}')

    # get_item_data(r'D:\Обучение парсингу\Parsing-training\lesson11\async_code\items_urls.txt')
    asyncio.run(gather_data(r'D:\Обучение парсингу\Parsing-training\lesson11\async_code\items_urls.txt'))
    finish_time = datetime.datetime.now()
    print(f'[TIME INFO] На сбор данных понадобилось {finish_time - time_after_receipt_urls}')

    print(f'[TIME INFO] На работу скрипта затрачено {finish_time - start_time}')


if __name__ == '__main__':
    main()
