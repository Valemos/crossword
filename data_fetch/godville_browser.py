import json
import time
from pathlib import Path

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver as Browser

from data_fetch.human_random import long_reaction_delay

_cookies_path = Path("cookies.json")


def load_cookies(browser):
    with _cookies_path.open("r") as fin:
        cookies = json.load(fin)

    for cookie in cookies:
        browser.add_cookie(cookie)


def godville_browser(subpage=''):
    options = Options()
    options.binary = "/home/anton/tools/firefox/firefox"
    browser = Browser(options=options)
    browser.get("https://godville.net/" + subpage)
    load_cookies(browser)
    time.sleep(long_reaction_delay())
    browser.refresh()
    return browser
