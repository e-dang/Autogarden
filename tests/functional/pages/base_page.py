from ..base import wait_for
from .elements import Button


class HomeButton(Button):
    LOCATOR = 'navBarHome'


class GardenDetailButton(Button):
    LOCATOR = 'navGardenDetail'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.home_button = HomeButton(self)
        self.garden_detail_nav_button = GardenDetailButton(self)

    def _get_inner_text(self, id_):
        return wait_for(lambda: self.driver.find_element_by_id(id_).get_attribute('innerText'))
