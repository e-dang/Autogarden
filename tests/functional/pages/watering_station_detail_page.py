import re

from .base_page import BasePage
from .elements import Button


class EditButton(Button):
    LOCATOR = 'editButton'


class WateringStationDetailPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.edit_button = EditButton(self)

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/watering-stations/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None
