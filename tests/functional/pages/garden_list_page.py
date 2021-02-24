import re

from garden.forms import NEW_GARDEN_SUBMIT_ID
from selenium.common.exceptions import WebDriverException

from ..base import wait
from .elements import TextInput


class NewGardenNameInput(TextInput):
    LOCATOR = 'id_name'


class NumWateringStationsInput(TextInput):
    LOCATOR = 'id_num_watering_stations'


class GardenListPage:
    new_garden_name = NewGardenNameInput()
    num_watering_stations = NumWateringStationsInput()

    def __init__(self, driver):
        self.driver = driver

    def has_correct_url(self):
        pattern = r'/gardens/$'
        return re.search(pattern, self.driver.current_url) is not None

    def click_add_new_garden(self):
        self.driver.find_element_by_id('addNewGardenBtn').click()

    def get_number_of_gardens(self):
        gardens = self._get_garden_list()
        return len(gardens.find_elements_by_css_selector('.card'))

    def submit_new_garden(self):
        self.driver.find_element_by_id(NEW_GARDEN_SUBMIT_ID).click()

    @wait
    def wait_for_garden_in_list(self, name):
        for element in self.driver.find_elements_by_css_selector('.card-title'):
            if element.get_attribute('innerText') == name:
                return element

        raise WebDriverException

    def click_garden(self, name):
        self.wait_for_garden_in_list(name).click()

    def _get_garden_list(self):
        return self.driver.find_element_by_id('gardenList')
