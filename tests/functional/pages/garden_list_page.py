import re

from garden.forms import NewGardenForm
from selenium.common.exceptions import WebDriverException

from ..base import wait
from .elements import Button, ImageInput, TextInput
from .base_page import BasePage


class NewGardenNameInput(TextInput):
    LOCATOR = 'id_name'


class NumWateringStationsInput(TextInput):
    LOCATOR = 'id_num_watering_stations'


class NewGardenButton(Button):
    LOCATOR = 'addNewGardenBtn'


class SubmitNewGardenButton(Button):
    LOCATOR = NewGardenForm.NEW_GARDEN_SUBMIT_ID


class GardenImageInput(ImageInput):
    INPUT_LOCATOR = 'id_image'


class CancelNewGardenButton(Button):
    LOCATOR = NewGardenForm.CANCEL_NEW_GARDEN_BTN_ID


class GardenListPage(BasePage):
    new_garden_name = NewGardenNameInput()
    num_watering_stations = NumWateringStationsInput()
    garden_image = GardenImageInput()

    def __init__(self, driver):
        super().__init__(driver)
        self.new_garden_button = NewGardenButton(self)
        self.submit_new_garden_button = SubmitNewGardenButton(self)
        self.cancel_new_garden_button = CancelNewGardenButton(self)
        self.modal_id = NewGardenForm.NEW_GARDEN_MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_of_gardens(self):
        gardens = self._get_garden_list()
        return len(gardens.find_elements_by_css_selector('.card'))

    @wait
    def wait_for_garden_in_list(self, name):
        for element in self.driver.find_elements_by_css_selector('.card-title'):
            if element.get_attribute('innerText') == name:
                return element

        raise WebDriverException('Could not find garden with that name')

    def get_garden_image(self, name):
        for card in self.driver.find_elements_by_css_selector('.card'):
            if card.find_elements_by_css_selector('.card-title')[0].get_attribute('innerText') == name:
                return card.find_elements_by_css_selector('.card-img-top')[0].get_attribute('src')

        raise WebDriverException('Could not find garden with that name')

    def click_garden(self, name):
        self.wait_for_garden_in_list(name).click()

    def _get_garden_list(self):
        return self.driver.find_element_by_id('gardenList')
