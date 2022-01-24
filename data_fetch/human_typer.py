import time

from selenium.webdriver.remote.webelement import WebElement

from data_fetch.human_random import *


class HumanTyper:

    def __init__(self, browser) -> None:
        self._browser = browser

    def type(self, element: WebElement, string: str):
        for character in string:
            self.type_once(element, character)

    @staticmethod
    def type_once(element: WebElement, character: str):
        element.send_keys(character)
        if character.isalpha():
            delay = keyboard_type_delay()
        else:
            delay = reaction_delay()
        time.sleep(delay)
