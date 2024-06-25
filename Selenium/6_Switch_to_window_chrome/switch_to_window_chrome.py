from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from fake_useragent import FakeUserAgent

ua = FakeUserAgent()

url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty"

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument(f'user-agent={ua.random}')
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

try:
    driver.get(url=url)
    time.sleep(5)

    items = driver.find_elements(By.CLASS_NAME, 'iva-item-sliderLink-uLz1v')
    items[0].click()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])  # Перемещаемся по вкладкам

    price = driver.find_elements(By.CLASS_NAME, 'style-price-value-main-TIg6u')[1]
    print(price)
    driver.close()

    driver.switch_to.window(driver.window_handles[0])

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
