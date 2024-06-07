import random
from time import sleep

from bs4 import BeautifulSoup
import requests
import json
import csv

# URL = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
#
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
}
#
# response = requests.get(URL, headers=headers).text
#
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(response)

# with open('index.html', 'r', encoding='utf-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# categories = soup.find_all('a', {'class': 'mzr-tc-group-item-href'})
#
# all_categories_dict = {}
# for category in categories:
#     link = 'https://health-diet.ru' + category['href']
#     text = category.text
#     all_categories_dict[text] = link
#
# with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
#     # indent делает отступы, ensure_ascii убирает экранирование и позволяет нормально  работать с кириллицей
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_dict.json', 'r', encoding='utf-8') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
print(f'Всего итераций: {iteration_count}')
count = 0
for category_name, category_link in all_categories.items():
    rep = [' ', '.', ',', "'"]
    for char in rep:
        if char in category_name:
            category_name = category_name.replace(char, '_')

    req = requests.get(url=category_link, headers=headers)
    src = req.text
    with open(f"data/{count}_{category_name}.html", 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Проверка страницы на наличие таблицы
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    # Собираем заголовки таблицы
    table_headers = soup.find(class_='mzr-tc-group-table').find_all('th')

    product = table_headers[0].text
    calories = table_headers[1].text
    proteins = table_headers[2].text
    fats = table_headers[3].text
    carbohydrates = table_headers[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # Собираем данные продуктов
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    products_info = []
    for product in products_data:
        product_data = product.find_all('td')

        product_name = product_data[0].find('a').text
        product_calories = product_data[1].text
        product_proteins = product_data[2].text
        product_fats = product_data[3].text
        product_carbohydrates = product_data[4].text

        products_info.append(
            {
                'Name': product_name,
                'Calories': product_calories,
                'Proteins': product_proteins,
                'Fats': product_fats,
                'Carbohydrates': product_carbohydrates
            }
        )

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    product_name,
                    product_calories,
                    product_proteins,
                    product_fats,
                    product_carbohydrates
                )
            )

    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итерация {count}. {category_name} записан...')
    iteration_count -= 1

    if iteration_count == 0:
        print('Работа закончена')
        break

    print(f'Осталось итераций: {iteration_count}')
    sleep(random.randrange(2, 4))
