from selenium import webdriver
import time

from selenium.webdriver.common.by import By

from auth_data import login, password

url = 'https://vk.com/'

driver = webdriver.Firefox()

TIME_SLEEP = 2

try:
    driver.get(url=url)
    time.sleep(TIME_SLEEP)

    email_input = driver.find_element(By.ID, 'index_email')
    email_input.clear()
    email_input.send_keys(login)
    time.sleep(TIME_SLEEP)

    driver.find_element(By.CLASS_NAME, 'VkIdCheckbox__checkboxOn').click()
    time.sleep(TIME_SLEEP)

    driver.find_element(By.CLASS_NAME, 'VkIdForm__signInButton').click()
    time.sleep(TIME_SLEEP)

    div_btn = driver.find_element(By.CLASS_NAME, 'vkc__ConfirmOTP__buttonGroup')
    div_btn.find_element(By.TAG_NAME, 'button').click()
    time.sleep(TIME_SLEEP)

    elements = driver.find_elements(By.CLASS_NAME, 'vkuiSimpleCell--mult')
    elements[-1].click()
    time.sleep(TIME_SLEEP)

    password_input = driver.find_element(By.NAME, 'password')
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(TIME_SLEEP)

    driver.find_element(By.CLASS_NAME, 'vkuiButton__in').click()
    time.sleep(TIME_SLEEP * 3)

    ordered_list = driver.find_element(By.TAG_NAME, 'ol')
    ordered_list.find_element(By.TAG_NAME, 'li').click()
    time.sleep(6)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
