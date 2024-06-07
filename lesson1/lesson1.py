import re

from bs4 import BeautifulSoup

with open('blank/index.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
# title = soup.title  # Получает тег + содержимое тега
# print(title)  # <title>Главная страница блога</title>
# print(title.text)  # Главная страница блога
# print(title.string)  # Главная страница блога

# .find() .find_all()
# h1_tag = soup.find('h1')  # Найдёт первый сверху тег h1
# h1_tags = soup.find_all('h1')  # Найдёт все теги h1 и запишет их в список

# user_name = soup.find('div', class_='user__name')  # Получаем текст тега div с классом user__name
# print(user_name.text.strip())  # Mr Anderson

# user_name = soup.find('div', class_='user__name').find('span').text
# print(user_name)  # Mr Anderson

# В словарь можно добавлять доп критерии отбора
# user_name = soup.find('div', {'class': 'user__name'}).find('span').text
# print(user_name)

# all_span_in_user_info = soup.find('div', class_='user__info').find_all('span')
# print(all_span_in_user_info)
#
# for tag in all_span_in_user_info:
#     print(tag.text)

# Спарсить ссылки на соцсети. Метод углубления внутрь по тегам
# social_links = soup.find(class_='social__networks').find('ul').find_all('a')
# print(social_links)
#
# for item in social_links:
#     link = item.get('href')
#     link2 = item['href']  # Аналогичный способ получения атрибута
#     text = item.text
#     print(f'{text}: {link}')

# .find_parent .find_parents
# post_div = soup.find(class_='post__text').find_parent()  # Поиск первого родителя
# print(post_div)

# Ищем ближайщего родителя с тегом div и классом user__post
# post_div = soup.find(class_='post__text').find_parent('div', class_='user__post')
# print(post_div)

# post_div = soup.find(class_='post__text').find_parents()  # Поднимается по иерархии до самого верха до html тега
# print(post_div)

# post_div = soup.find(class_='post__text').find_parents('div', class_='user__post')  # Поднимается до ограничения
# print(post_div)

# .next_element .previous_element
# next_el = soup.find(class_='post__title').next_element  # Вернёт перенос строки (пустая строка будет в выводе)
# next_el = soup.find(class_='post__title').next_element.next_element.text  # Вернёт тег, следующий за post__title
# print(next_el)

# next_el = soup.find(class_='post__title').find_next().text  # Ищет следующий элемент
# print(next_el)

# .find_next_sibling() .find_previous_sibling()  # Ищут элементы на этом же уровне вложенности
# next_sib = soup.find(class_='post__title').find_next_sibling()  # Будет взят тег с классом post__text
# print(next_sib)

# find_by_text = soup.find('span', string=re.compile("Mr"))  # Поиск по текстовому содержанию
# print(find_by_text)

# find_all_Mr = soup.find_all(string=re.compile("([Mm]r)"))
# print(find_all_Mr)
