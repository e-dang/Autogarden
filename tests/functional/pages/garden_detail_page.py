import re

from selenium.common.exceptions import NoSuchElementException
from tests.functional.base import wait_for

from .base_page import BasePage
from .elements import Button, ButtonGroup


class WateringStationButtons(ButtonGroup):
    LOCATOR = 'wateringStation'


class AddWateringStationButton(Button):
    LOCATOR = 'addWateringStationBtn'


class DeactivateButton(Button):
    LOCATOR = 'deactivateAllBtn'


class EditButton(Button):
    LOCATOR = 'editButton'


class ActivateButton(Button):
    LOCATOR = 'activateAllBtn'


class GardenDetailPage(BasePage):
    watering_station = WateringStationButtons()

    FIELD_NOT_FOUND = -1

    def __init__(self, driver):
        super().__init__(driver)
        self.field_mapping = None
        self.add_watering_station_button = AddWateringStationButton(self)
        self.deactivate_button = DeactivateButton(self)
        self.activate_button = ActivateButton(self)
        self.edit_button = EditButton(self)

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

    def get_water_station_data_from_table(self, ws_idx):
        ws_status = self.get_watering_station_field_value(ws_idx, 'Status')
        plant_type = self.get_watering_station_field_value(ws_idx, 'Plant Type')
        moisture_threshold = self.get_watering_station_field_value(ws_idx, 'Moisture Threshold')
        watering_duration = self.get_watering_station_field_value(ws_idx, 'Watering Duration')
        return {
            'status': ws_status,
            'plant_type': plant_type,
            'moisture_threshold': moisture_threshold,
            'watering_duration': watering_duration
        }

    def get_garden_status(self):
        return self._get_inner_text('connectionStatus')

    def get_last_connected_from(self):
        return self._get_inner_text('lastConnectionFrom')

    def get_last_connected_at(self):
        return self._get_inner_text('lastConnectedAt')

    def get_next_expected_update(self):
        return self._get_inner_text('nextExpectedUpdate')

    def get_water_level(self):
        return self._get_inner_text('waterLevel')

    def get_garden_name(self):
        return self._get_inner_text('gardenName')

    def get_garden_image_src(self):
        return wait_for(lambda: self.driver.find_element_by_id('gardenImage')).get_attribute('src')

    def get_connection_strength(self):
        return self._get_inner_text('connectionStrength')

    def get_update_frequency(self):
        return self._get_inner_text('updateFrequency')

    def is_displaying_info_for_garden(self, garden):
        return all([
            self.get_garden_status() == garden.status,
            self.get_last_connected_from() == str(garden.last_connection_ip),
            self.get_last_connected_at() == garden.get_formatted_last_connection_time(),
            self.get_update_frequency() == garden.update_frequency_display(),
            self.get_connection_strength() == garden.get_connection_strength_display(),
            self.get_water_level() == str(garden.get_water_level_display()),
        ])

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
