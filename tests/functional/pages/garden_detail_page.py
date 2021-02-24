import re

from garden.forms import UPDATE_WATERING_STATION_SUBMIT_ID

from .base_page import BasePage
from .elements import ButtonGroup, TextInput


class WateringStationButtons(ButtonGroup):
    LOCATOR = 'wateringStationBtn'


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class GardenDetailPage(BasePage):
    watering_station = WateringStationButtons()
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_watering_stations(self):
        return len(self.driver.find_elements_by_css_selector('button[id*=wateringStationBtn]'))

    def submit_watering_station_update(self):
        self.driver.find_element_by_id(UPDATE_WATERING_STATION_SUBMIT_ID).click()
