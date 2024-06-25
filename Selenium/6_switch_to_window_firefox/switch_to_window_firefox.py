from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from fake_useragent import FakeUserAgent

ua = FakeUserAgent()
url = 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty'

options = webdriver.FirefoxOptions()
options.set_preference('general.useragent.override', f'{ua.random}')

driver = webdriver.Firefox(options=options)

try:
    driver.get(url=url)
    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
