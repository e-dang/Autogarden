from ..base import wait_for
from .elements import Button


class HomeButton(Button):
    LOCATOR = 'AutoGarden'
    BY = 'find_element_by_link_text'


class GardenDetailButton(Button):
    LOCATOR = 'navGardenDetail'


class LogoutButton(Button):
    LOCATOR = 'Logout'
    BY = 'find_element_by_link_text'


class SettingsButton(Button):
    LOCATOR = 'Settings'
    BY = 'find_element_by_link_text'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.home_button = HomeButton(self)
        self.garden_detail_nav_button = GardenDetailButton(self)
        self.logout_button = LogoutButton(self)
        self.settings_button = SettingsButton(self)

    def _get_inner_text(self, id_):
        return wait_for(lambda: self.driver.find_element_by_id(id_).get_attribute('innerText'))
