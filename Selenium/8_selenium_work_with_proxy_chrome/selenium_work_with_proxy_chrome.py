from selenium import webdriver
import time
import os
from proxy6_auth import LOGIN_US, PASSWORD_US
import zipfile
from fake_useragent import FakeUserAgent

ua = FakeUserAgent()

PROXY_HOST = '23.236.128.4'  # ip
PROXY_PORT = 8000  # port
PROXY_USER = LOGIN_US  # login
PROXY_PASS = PASSWORD_US  # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if use_proxy:
        # chrome_options.add_argument('--proxy-server=23.236.128.4:8000')

        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr("background.js", background_js)

        chrome_options.add_extension(plugin_file)

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def main():
    user = ua.random
    print(user)
    driver = get_chromedriver(use_proxy=True, user_agent=f'{user}')
    driver.maximize_window()
    driver.get(url='https://2ip.ru')
    time.sleep(15)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
