from selenium import webdriver
from fake_useragent import UserAgent
import time

url = 'https://vk.com/'
options = webdriver.FirefoxOptions()
ua = UserAgent()
options.set_preference(f'general.useragent.override', ua.random)
driver = webdriver.Firefox(options=options)

try:
    driver.get(url=url)  # Открыть ссылку в браузере
    # driver.save_screenshot('vk.png')  # Делает скриншот, можно ещё get_screenshot_as_file('Путь куда сохранить')
    time.sleep(2)
except Exception as ex:
    print(ex)
finally:
    driver.close()  # Закрыть драйвер
    driver.quit()
