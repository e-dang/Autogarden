import re

from garden.forms import WateringStationForm

from ..base import wait_for
from .base_page import BasePage
from .elements import CancelButton, DeleteButton, TextInput, ToggleButton, SubmitButton, ConfirmDeleteButton


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class PlantTypeInput(TextInput):
    LOCATOR = 'id_plant_type'


class StatusCheckBox(ToggleButton):
    LOCATOR = 'id_status'


class WateringStationUpdatePage(BasePage):
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()
    plant_type = PlantTypeInput()
    status = StatusCheckBox()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)
        self.delete_button = DeleteButton(self)
        self.cancel_button = CancelButton(self)
        self.confirm_delete_button = ConfirmDeleteButton(self)
        self.modal_id = WateringStationForm.MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/watering-stations/[0-9]+/update/$'
        return re.search(pattern, self.driver.current_url) is not None

    def go_to_watering_station_page(self, ws_num):
        wait_for(lambda: self.driver.find_element_by_id('navWateringStations')).click()
        wait_for(lambda: self.driver.find_element_by_id(f'navWateringStation{ws_num}')).click()

    def update_info(self, status=None, plant_type=None, moisture_threshold=None, watering_duration=None):
        if status is not None:
            self.status = status
        if plant_type is not None:
            self.plant_type = plant_type
        if moisture_threshold is not None:
            self.moisture_threshold = moisture_threshold
        if watering_duration is not None:
            self.watering_duration = watering_duration
        self.submit_button.click()
