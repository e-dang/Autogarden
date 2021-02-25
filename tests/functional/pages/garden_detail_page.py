import re

from .base_page import BasePage
from .elements import ButtonGroup
from selenium.common.exceptions import NoSuchElementException


class WateringStationButtons(ButtonGroup):
    LOCATOR = 'wateringStation'


class GardenDetailPage(BasePage):
    watering_station = WateringStationButtons()

    FIELD_NOT_FOUND = -1

    def __init__(self, driver):
        super().__init__(driver)
        self.field_mapping = None

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_watering_stations(self):
        return len(self.driver.find_elements_by_css_selector('tbody tr'))

    def field_is_in_watering_station_table(self, field_name):
        return False if self._get_field_index(field_name) == GardenDetailPage.FIELD_NOT_FOUND else True

    def get_watering_station_field_value(self, ws_idx, field_name):
        idx = self._get_field_index(field_name)
        if idx == GardenDetailPage.FIELD_NOT_FOUND:
            raise NoSuchElementException

        rows = self.driver.find_elements_by_css_selector('tbody > tr')
        cols = rows[ws_idx - 1].find_elements_by_tag_name('td')
        return cols[idx].get_attribute('innerText')

    def _get_field_index(self, field_name):
        if self.field_mapping is None:
            self._cache_field_mappings()

        if field_name in self.field_mapping:
            return self.field_mapping[field_name]
        return GardenDetailPage.FIELD_NOT_FOUND

    def _cache_field_mappings(self):
        self.field_mapping = {}
        for i, header in enumerate(self.driver.find_elements_by_css_selector('th')):
            self.field_mapping[header.get_attribute('innerText')] = i
