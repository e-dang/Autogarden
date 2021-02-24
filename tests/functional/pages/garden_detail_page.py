import re

from .elements import ButtonGroup, TextInput


class WateringStationButtons(ButtonGroup):
    LOCATOR = 'wateringStationBtn'


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration_input'


class GardenDetailPage:
    watering_station = WateringStationButtons()
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()

    def __init__(self, driver):
        self.driver = driver

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_watering_stations(self):
        return len(self.driver.find_elements_by_css_selector('button[id*=wateringStationBtn]'))
