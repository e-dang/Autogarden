import re

from .base_page import BasePage
from .elements import ButtonGroup


class WateringStationButtons(ButtonGroup):
    LOCATOR = 'wateringStationBtn'


class GardenDetailPage(BasePage):
    watering_station = WateringStationButtons()

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_watering_stations(self):
        return len(self.driver.find_elements_by_css_selector('button[id*=wateringStationBtn]'))
