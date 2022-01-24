import time

import numpy as np
import scipy.interpolate as si
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from .human_random import *

class HumanMouse:

    def __init__(self, browser) -> None:
        self.action = ActionChains(browser)

    def move(self, start_element: WebElement, end_element: WebElement):
        start_position = self.get_position(start_element)
        end_position = self.get_position(end_element)
        self.move_instant(start_element)

        self.move_instant(end_element)
        # curve = self.generate_curve(start_position, end_position)
        # self.move_by_curve(curve)

    @staticmethod
    def get_position(element: WebElement):
        return element.location['x'], element.location['y']

    def move_instant(self, start_element: WebElement):
        self.action.move_to_element(start_element)
        self.action.perform()

    def move_by_curve(self, curve):
        for mouse_x, mouse_y in self.interpolate_curve(curve):
            self.action.move_by_offset(mouse_x, mouse_y)
            self.action.perform()

    @staticmethod
    def generate_curve(start, end):
        # todo: create path
        return []

    @staticmethod
    def interpolate_curve(points):
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=3)
        y_tup = si.splrep(t, y, k=3)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        yield from zip(si.splev(ipl_t, x_list), si.splev(ipl_t, y_list))

    @staticmethod
    def click(element: WebElement):
        time.sleep(reaction_delay())
        element.click()
