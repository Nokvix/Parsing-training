from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from fake_useragent import FakeUserAgent
from multiprocessing import Pool

ua = FakeUserAgent()

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument(f'user-agent={ua.random}')
options.add_argument('--disable-blink-features=AutomationControlled')

urls_list = ["https://stackoverflow.com", "https://instagram.com", "https://vk.com"]


# def get_data(url: str):
#     try:
#         driver = webdriver.Chrome(options=options)
#         driver.get(url=url)
#         time.sleep(5)
#
#         driver.get_screenshot_as_file(f'media/{url.split("//")[1]}.png')
#     except Exception as ex:
#         print(ex)
#     finally:
#         driver.close()
#         driver.quit()
#
#
# if __name__ == '__main__':
#     p = Pool(len(urls_list))
#     p.map(get_data, urls_list)


def get_data(url: str):
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url=url)
        time.sleep(5)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    p = Pool(len(urls_list))
    p.map(get_data, urls_list)
