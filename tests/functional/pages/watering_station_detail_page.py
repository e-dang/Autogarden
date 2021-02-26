from garden.models import WateringStation
import re

from garden.forms import UPDATE_WATERING_STATION_SUBMIT_ID

from .base_page import BasePage
from .elements import TextInput, ToggleButton
from ..base import wait_for


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class PlantTypeInput(TextInput):
    LOCATOR = 'id_plant_type'


class StatusCheckBox(ToggleButton):
    LOCATOR = 'id_status'


class WateringStationDetailPage(BasePage):
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()
    plant_type = PlantTypeInput()
    status = StatusCheckBox()

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/watering-stations/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def submit_watering_station_update(self):
        self.driver.find_element_by_id(UPDATE_WATERING_STATION_SUBMIT_ID).click()

    def go_back_to_garden_detail(self):
        wait_for(lambda: self.driver.find_element_by_id('navGardenDetail')).click()

    def go_to_watering_station_page(self, ws_num):
        wait_for(lambda: self.driver.find_element_by_id('navWateringStations')).click()
        wait_for(lambda: self.driver.find_element_by_id(f'navWateringStation{ws_num}')).click()
