import re

from garden.forms import UPDATE_WATERING_STATION_SUBMIT_ID

from .base_page import BasePage
from .elements import TextInput


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class WateringStationDetailPage(BasePage):
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/watering-stations/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def submit_watering_station_update(self):
        self.driver.find_element_by_id(UPDATE_WATERING_STATION_SUBMIT_ID).click()

    def go_back_to_garden_detail(self):
        self.driver.find_element_by_id(f'navGardenDetail').click()

    def go_to_watering_station_page(self, ws_num):
        self.driver.find_element_by_id(f'navWateringStation{ws_num}').click()
