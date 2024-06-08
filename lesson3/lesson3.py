import requests
from bs4 import BeautifulSoup
import json

URL = 'http://www.edutainme.ru'


def get_data(url):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'
    }

    req = requests.get(URL, headers=headers).text
    return req


data = get_data(URL)
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(data)
