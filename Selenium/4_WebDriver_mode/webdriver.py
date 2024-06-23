from selenium import webdriver
import time

url = 'https://vk.com/'

options = webdriver.FirefoxOptions()

# user-agent
options.set_preference('general.useragent.override',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36')

# disable webdriver mode
options.set_preference("dom.webdriver.enabled", False)  # Не работает

driver = webdriver.Firefox(options=options)

try:
    driver.get(url='https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
