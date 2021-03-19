import re

from garden.forms import NewGardenForm
from selenium.common.exceptions import WebDriverException

from ..base import wait
from .elements import Button, CropButton, ImageInput, ResetButton, SubmitButton, TextInput, CancelButton
from .base_page import BasePage


class NewGardenNameInput(TextInput):
    LOCATOR = 'id_name'


class NumWateringStationsInput(TextInput):
    LOCATOR = 'id_num_watering_stations'


class NewGardenButton(Button):
    LOCATOR = 'addNewGardenBtn'


class GardenImageInput(ImageInput):
    INPUT_LOCATOR = 'id_image'


class UpdateFrequency(TextInput):
    LOCATOR = 'id_update_frequency'


class GardenListPage(BasePage):
    new_garden_name = NewGardenNameInput()
    num_watering_stations = NumWateringStationsInput()
    garden_image = GardenImageInput()
    update_frequency = UpdateFrequency()

    def __init__(self, driver):
        super().__init__(driver)
        self.new_garden_button = NewGardenButton(self)
        self.submit_button = SubmitButton(self)
        self.cancel_button = CancelButton(self)
        self.crop_image_button = CropButton(self)
        self.reset_image_button = ResetButton(self)
        self.modal_id = NewGardenForm.MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_of_gardens(self):
        return len(self.driver.find_elements_by_css_selector('.list-group-item'))

    @wait
    def wait_for_garden_in_list(self, name):
        for element in self.driver.find_elements_by_tag_name('h2'):
            if element.get_attribute('innerText') == name:
                return element

        raise WebDriverException('Could not find garden with that name')

    def get_garden_image(self, name):
        for card in self.driver.find_elements_by_css_selector('.list-group-item'):
            if card.find_element_by_tag_name('h2').get_attribute('innerText') == name:
                return card.find_element_by_tag_name('img').get_attribute('src')

        raise WebDriverException('Could not find garden with that name')

    def click_garden(self, name):
        self.wait_for_garden_in_list(name).click()

    def add_garden(self, garden_name, num_watering_stations, garden_image, update_frequency):
        self.new_garden_button.click()
        self.new_garden_name = garden_name
        self.num_watering_stations = num_watering_stations
        self.garden_image = garden_image
        self.update_frequency = update_frequency
        self.crop_image_button.click()
        self.submit_button.click()
