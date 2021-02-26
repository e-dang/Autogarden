import re

from garden.models import WateringStation
from selenium.common.exceptions import NoSuchElementException

from .base_page import BasePage
from .elements import ButtonGroup


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

    def get_status(self):
        return self._get_inner_text('connectionStatus')

    def get_last_connected_from(self):
        return self._get_inner_text('lastConnectionFrom')

    def get_last_connected_at(self):
        return self._get_inner_text('lastConnectedAt')

    def get_next_expected_update(self):
        return self._get_inner_text('nextExpectedUpdate')

    def get_num_missed_updates(self):
        return self._get_inner_text('numMissedUpdates')

    def get_water_level(self):
        return self._get_inner_text('waterLevel')

    def convert_watering_station_status_to_bool(self, status):
        return WateringStation.ACTIVE_STATUS_STR if status else WateringStation.INACTIVE_STATUS_STR

    def _get_inner_text(self, id_):
        return self.driver.find_element_by_id(id_).get_attribute('innerText')

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
