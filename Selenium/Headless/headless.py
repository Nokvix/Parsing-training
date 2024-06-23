from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from auth_data import login, password
import pickle

url = 'https://vk.com/'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)


TIME_SLEEP = 2

try:
    driver.get(url=url)
    time.sleep(TIME_SLEEP)

    print('Ввожу логин')
    email_input = driver.find_element(By.ID, 'index_email')
    email_input.clear()
    email_input.send_keys(login)
    time.sleep(TIME_SLEEP)

    print('Убираю галочку')
    driver.find_element(By.CLASS_NAME, 'VkIdCheckbox__checkboxOn').click()
    time.sleep(TIME_SLEEP)

    print('Нажимаю войти')
    driver.find_element(By.CLASS_NAME, 'VkIdForm__signInButton').click()
    time.sleep(TIME_SLEEP)

    print('Выбираю другой способ авторизации')
    div_btn = driver.find_element(By.CLASS_NAME, 'vkc__ConfirmOTP__buttonGroup')
    div_btn.find_element(By.TAG_NAME, 'button').click()
    time.sleep(TIME_SLEEP)

    print('Выбираю пароль')
    elements = driver.find_elements(By.CLASS_NAME, 'vkuiSimpleCell--mult')
    elements[-1].click()
    time.sleep(TIME_SLEEP)

    print('Ввожу пароль')
    password_input = driver.find_element(By.NAME, 'password')
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(TIME_SLEEP)

    driver.find_element(By.CLASS_NAME, 'vkuiButton__in').click()
    print('Вошёл в ВК')
    time.sleep(TIME_SLEEP * 3)

    ordered_list = driver.find_element(By.TAG_NAME, 'ol')
    ordered_list.find_element(By.TAG_NAME, 'li').click()
    print('Перешёл на "Моя страница"')
    time.sleep(6)

    driver.find_element(By.CLASS_NAME, 'VideoPreview-module__videoImage--h3ni6').click()
    print('Открыл видео')
    time.sleep(TIME_SLEEP * 5)
    print('Закончил смотреть видео')

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
