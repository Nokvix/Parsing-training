import random
import time
import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import FakeUserAgent
from selenium import webdriver
from typing import Dict, Union

ua = FakeUserAgent()
counter = 0


def get_correct_price(price_str: str):
    price_fin = ''
    for char in price_str:
        if char.isdigit():
            price_fin += char
    return int(price_fin)


def create_driver(id_product):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)

    url = f'https://www.wildberries.ru/catalog/{id_product}/detail.aspx'

    driver.get(url=url)
    time.sleep(5)

    return driver


def get_product_page(driver):
    # with open(f'{id_product}_product.html', 'w', encoding='utf-8') as file:
    #     file.write(driver.page_source)

    return driver.page_source


def get_wallet_price(page):
    soup = BeautifulSoup(page, 'lxml')
    wallet_price = get_correct_price(soup.find('span', class_='price-block__wallet-price').text.strip())

    return wallet_price


def get_main_data(page, id_product):
    soup = BeautifulSoup(page, 'lxml')

    name_product = soup.find('h1').text.strip()
    price = get_correct_price(soup.find('ins', class_='price-block__final-price').text.strip())
    product_url = f'https://www.wildberries.ru/catalog/{id_product}/detail.aspx'

    product_data = {
        'id': id_product,
        'price': price,
        'url': product_url,
        'name': name_product,
    }

    return product_data


def scraping_page(id_product, driver):
    global counter
    page = get_product_page(driver)
    # with open(f'{id_product}_product.html', 'r', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file.read(), 'lxml')

    # Получаем основные данные
    try:
        product_data = get_main_data(page, id_product)

    except Exception as ex:
        print('Main data.', ex)
        if counter == 7:
            print('Не удалось получить данные. Попробуйте позже')
            return None

        driver.refresh()
        time.sleep(2)

        counter += 1
        print(f'Попытка {counter}')

        product_data = scraping_page(id_product, driver)

    # Получаем цену с WB кошельком
    counter = 0
    try:
        wallet_price = get_wallet_price(driver.page_source)
        product_data['wallet_price'] = wallet_price
    except Exception as ex:
        print(f'Wallet price. {ex}')
        if counter == 7:
            print('Не удалось получить цену с WB кошельком...')
            product_data['wallet_price'] = 'Неизвестно. Узнайте её, перейдя по ссылке'
            return product_data

        driver.refresh()
        time.sleep(2)
        wallet_price = get_wallet_price(driver.page_source)
        if wallet_price is not None:
            product_data['wallet_price'] = wallet_price
        else:
            print(f'Не удалось получить цену с WB кошельком. Попытка {counter}')
            counter += 1

    return product_data


def dict_to_string(data: Dict[str, Union[int, str]]):
    string = (f'Товар: {data["name"]}\n'
              f'Артикул: {data["id"]}\n'
              f'Цена с WB кошельком: {data["wallet_price"]}₽\n'
              f'Цена без WB кошелька: {data["price"]}₽\n'
              f'Ссылка на товар: {data["url"]}')

    return string


def main(id_product):
    driver = create_driver(id_product)
    product_data = scraping_page(id_product, driver)
    string = dict_to_string(product_data)

    driver.close()
    driver.quit()
    return string


if __name__ == '__main__':
    # product_data = main(201759187)
    string = main(input('Введите артикул товара: '))
    print(string)
