import re

from garden.formatters import GardenFormatter, WateringStationFormatter
from garden.forms import NewWateringStationForm
from selenium.common.exceptions import NoSuchElementException
from tests.functional.base import wait_for

from .base_page import BasePage
from .elements import Button, ButtonGroup, CropButton, EditButton, CancelButton, ImageInput, ResetButton, TextInput


class WateringStationButtons(ButtonGroup):
    LOCATOR = 'wateringStation'


class AddWateringStationButton(Button):
    LOCATOR = 'addWateringStationBtn'


class DeactivateButton(Button):
    LOCATOR = 'deactivateAllBtn'


class ActivateButton(Button):
    LOCATOR = 'activateAllBtn'


class SubmitButton(Button):
    LOCATOR = '//input[@type="submit" and @value="Create"]'
    BY = 'find_element_by_xpath'


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class WateringStationImageInput(ImageInput):
    INPUT_LOCATOR = 'id_image'


class GardenDetailPage(BasePage):
    watering_station = WateringStationButtons()
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()
    image = WateringStationImageInput()

    FIELD_NOT_FOUND = -1

    def __init__(self, driver):
        super().__init__(driver)
        self.field_mapping = None
        self.add_watering_station_button = AddWateringStationButton(self)
        self.deactivate_button = DeactivateButton(self)
        self.activate_button = ActivateButton(self)
        self.edit_button = EditButton(self)
        self.submit_button = SubmitButton(self)
        self.cancel_button = CancelButton(self)
        self.crop_image_button = CropButton(self)
        self.reset_image_button = ResetButton(self)
        self.modal_id = NewWateringStationForm.MODAL_ID

    def enter_form_fields(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_watering_station(self, **kwargs):
        self.enter_form_fields(**kwargs)
        self.submit_button.click()

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

    def is_table_row_displaying_data_for_watering_station(self, row, watering_station):
        formatter = WateringStationFormatter(watering_station)
        return all([
            self.get_watering_station_field_value(row, '#') == formatter.idx,
            self.get_watering_station_field_value(row, 'Plant Type') == formatter.plant_type,
            self.get_watering_station_field_value(row, 'Status') == formatter.status,
            self.get_watering_station_field_value(row, 'Moisture Threshold') == str(formatter.moisture_threshold),
            self.get_watering_station_field_value(row, 'Watering Duration') == formatter.watering_duration
        ])

    def get_garden_status(self):
        return self._get_inner_text('connectionStatus')

    def get_last_connected_from(self):
        return self._get_inner_text('lastConnectionFrom')

    def get_last_connected_at(self):
        return self._get_inner_text('lastConnectedAt')

    def get_api_key(self):
        return self._get_inner_text('apiKey')

    def get_water_level(self):
        return self._get_inner_text('waterLevel')

    def get_garden_name(self):
        return self._get_inner_text('name')

    def get_garden_image_src(self):
        return wait_for(lambda: self.driver.find_element_by_tag_name('img')).get_attribute('src')

    def get_connection_strength(self):
        return self._get_inner_text('connectionStrength')

    def get_update_frequency(self):
        return self._get_inner_text('updateFrequency')

    def is_displaying_info_for_garden(self, garden):
        formatter = GardenFormatter(garden)
        return all([
            self.get_garden_status() == formatter.get_is_connected_display(),
            self.get_last_connected_from() == str(formatter.last_connection_ip),
            self.get_last_connected_at() == formatter.get_last_connection_time_display(),
            self.get_update_frequency() == formatter.get_update_frequency_display(),
            self.get_connection_strength() == formatter.get_connection_strength_display(),
            self.get_water_level() == formatter.get_water_level_display(),
            self.get_api_key() == str(formatter.token.uuid)
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
