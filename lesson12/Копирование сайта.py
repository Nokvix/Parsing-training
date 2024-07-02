from fake_useragent import FakeUserAgent
from bs4 import BeautifulSoup
import requests
import random
import time
import json

ua = FakeUserAgent()


def get_response_text(url, page=None, retry=3):
    headers = {
        'Accept': '*/*',
        'User-Agent': f'{ua.random}'
    }

    try:
        response = requests.get(url=url, headers=headers)
        return response.text

    except Exception as ex:
        if retry == 0:
            raise Exception
        else:
            time.sleep(3)
            print(f'retry -> {retry}')

            return get_response_text(url, page, retry=(retry - 1))


def get_pages_data():
    page = 1
    is_last_page = False
    urls_list = []

    while True:
        time.sleep(random.randrange(1, 3))

        if is_last_page or page == 30:
            return

        url = f'https://hi-news.ru/page/{page}'
        try:
            page_html = get_response_text(url, page)

            soup = BeautifulSoup(page_html, 'lxml')
            page_number_li = soup.find('ul', class_='pagination').find_all('li')

            last_li = page_number_li[-1].text

            try:
                page_number = int(last_li)
                is_last_page = True

            except Exception as ex:
                pass

            links = soup.find_all('a', {'class': 'more-link', 'rel': 'nofollow'})

            with open(f'links.txt', 'a', encoding='utf-8') as file:
                for link in links:
                    urls_list.append(link['href'])
                    file.write(f"{link['href']}\n")

            with open(f'pages_html/{page}.html', 'w', encoding='utf-8') as file:
                file.write(page_html)

            print(f'Получил данные страницы {page}')
            page += 1

        except Exception as ex:
            print(f'Не получилось собрать данные со страницы {page}')
            continue


def get_item_data():
    with open('links.txt', 'r', encoding='utf-8') as file:
        links = [link.strip() for link in file.readlines()]

    articles_list = []

    counter = 0
    number_link = len(links)
    for link in links:
        counter += 1
        time.sleep(random.randrange(2, 4))
        try:
            response_text = get_response_text(link)

            soup = BeautifulSoup(response_text, 'lxml')

            try:
                author = soup.find('a', class_='author').text.strip()
            except Exception:
                author = None

            try:
                publication_date = soup.find('time', class_='post__date').text.strip()
            except Exception:
                publication_date = None

            try:
                title = soup.find('h1').text.strip()
            except Exception:
                title = None

            try:
                main_photo_src = soup.find('p', class_='wp-caption-text').findPrevious()['src']
            except Exception:
                main_photo_src = None

            try:
                text = soup.find('div', class_='text').text
            except Exception:
                text = None

            # print(title)
            # print(author)
            # print(publication_date)
            # print(main_photo_src)
            # print(text)
            # print('#'*50)

            articles_list.append(
                {
                    'title': title,
                    'author': author,
                    'publication_date': publication_date,
                    'text': text,
                    'main_photo_src': main_photo_src

                }
            )

            print(f'Обработал статью {counter}/{number_link}')

        except Exception as ex:
            print(f'Не удалось получить статью: {link}')
            continue

    with open('articles.json', 'w', encoding='utf-8') as file:
        json.dump(articles_list, file, indent=4, ensure_ascii=False)

    print('Закончил обработку статей')


def main():
    # get_pages_data()
    get_item_data()


if __name__ == '__main__':
    main()
