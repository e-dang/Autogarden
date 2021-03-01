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

    def get_status(self):
        return self._get_inner_text('status')

    def get_plant_type(self):
        return self._get_inner_text('plantType')

    def get_moisture_threshold(self):
        return self._get_inner_text('moistureThreshold')

    def get_watering_duration(self):
        return self._get_inner_text('wateringDuration')

    def get_ws_idx(self):
        return self._get_inner_text('wsIdx')
