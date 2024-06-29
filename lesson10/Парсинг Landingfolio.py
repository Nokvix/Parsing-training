import time

import requests
from bs4 import BeautifulSoup
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

image_count = 0
images_urls_list = []
landings_data_list = []


def save_json_data(page, retry=3):
    url = f'https://s3.landingfolio.com/inspiration?page={page}&sortBy=free-first'

    try:
        response = requests.get(url=url, headers=headers)
        json_data = json.loads(response.text)

        if not json_data:
            raise Exception

        if not os.path.exists('data_page_json'):
            os.mkdir('data_page_json')

        with open(f'data_page_json/{page}_json_data.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)

    except Exception as ex:
        if retry > 0:
            time.sleep(1)
            save_json_data(page, retry - 1)
        else:
            raise Exception


def get_page_count():
    page = 0
    while True:
        try:
            page += 1
            save_json_data(page)
            print(f'Сохранил данные {page} страницы')
            if page % 10 == 0:
                time.sleep(2)
        except Exception as ex:
            print('#' * 20)
            return page - 1


def get_landings_data(page_count):
    global image_count, landings_data_list, images_urls_list

    for page in range(1, page_count + 1):
        with open(f'data_page_json/{page}_json_data.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        for landing in json_data:
            try:
                landing_url = f'https://www.landingfolio.com/inspiration/post/{landing["slug"]}'
            except Exception:
                landing_url = 'no slug url'

            try:
                landing_title = landing['title']
            except Exception:
                landing_title = 'no title'

            try:
                website_url = landing['url']
            except Exception:
                website_url = 'no website url'

            screenshots_desktop = []
            screenshots_mobile = []
            for screenshot in landing['screenshots']:
                try:
                    title = screenshot['title']
                except Exception:
                    title = 'no title'

                try:
                    screenshot_url = f"https://landingfoliocom.imgix.net/{screenshot['images']['desktop']}"
                except Exception:
                    screenshot_url = 'no url'

                if screenshot_url != 'no url':
                    # images_urls_list.append(screenshot_url)

                    screenshots_desktop.append(
                        {
                            'title': title,
                            'url': screenshot_url
                        }
                    )

                    image_count += 1

                try:
                    title = screenshot['title']
                except Exception:
                    title = 'no title'

                try:
                    screenshot_url = f"https://landingfoliocom.imgix.net/{screenshot['images']['mobile']}"
                except Exception:
                    screenshot_url = 'no url'

                if screenshot_url != 'no url':
                    # images_urls_list.append(screenshot_url)

                    screenshots_mobile.append(
                        {
                            'title': title,
                            'url': screenshot_url
                        }
                    )

                    image_count += 1

            landings_data_list.append(
                {
                    'title': landing_title,
                    'website': website_url,
                    'landing_url': landing_url,
                    'screenshots_mobile': screenshots_mobile,
                    'screenshots_desktop': screenshots_desktop
                }
            )

        print(f'Собрал данные со страницы {page}/{page_count}')

    with open('all_landings_json.json', 'w', encoding='utf-8') as file:
        json.dump(landings_data_list, file, indent=4, ensure_ascii=False)

    # with open('images_urls.json', 'w', encoding='utf-8') as file:
    #     images_urls_dict = {
    #         'urls': images_urls_list
    #     }
    #     json.dump(images_urls_dict, file, indent=4, ensure_ascii=False)

    print('Сбор данных закончен')
    print(f'Сохранены ссылки на {image_count} изображений')


def main():
    page_count = get_page_count()
    get_landings_data(page_count)


if __name__ == '__main__':
    main()

# https://landingfoliocom.imgix.net/{inspiration/1684978900536Brevo20formerly20Sendinblue20mobile00bbd7249a8e49e3a83545c23c6f9a9dpng}
