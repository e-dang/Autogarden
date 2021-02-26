import re

from garden.forms import WateringStationForm, DeleteWateringStationForm

from ..base import wait_for
from .base_page import BasePage
from .elements import Button, TextInput, ToggleButton


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class PlantTypeInput(TextInput):
    LOCATOR = 'id_plant_type'


class StatusCheckBox(ToggleButton):
    LOCATOR = 'id_status'


class WateringStationFormSubmitButton(Button):
    LOCATOR = WateringStationForm.UPDATE_WATERING_STATION_SUBMIT_ID


class DeleteButton(Button):
    LOCATOR = WateringStationForm.DELETE_BUTTON_ID


class CancelDeleteButton(Button):
    LOCATOR = DeleteWateringStationForm.CANCEL_DELETE_BTN_ID


class ConfirmDeleteButton(Button):
    LOCATOR = DeleteWateringStationForm.CONFIRM_DELETE_BTN_ID


class WateringStationDetailPage(BasePage):
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()
    plant_type = PlantTypeInput()
    status = StatusCheckBox()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = WateringStationFormSubmitButton(self)
        self.delete_button = DeleteButton(self)
        self.cancel_delete_button = CancelDeleteButton(self)
        self.confirm_delete_button = ConfirmDeleteButton(self)
        self.modal_id = WateringStationForm.DELETE_WATERING_STATION_MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/watering-stations/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def submit_watering_station_update(self):
        self.driver.find_element_by_id(WateringStationForm.UPDATE_WATERING_STATION_SUBMIT_ID).click()

    def go_back_to_garden_detail(self):
        wait_for(lambda: self.driver.find_element_by_id('navGardenDetail')).click()

    def go_to_watering_station_page(self, ws_num):
        wait_for(lambda: self.driver.find_element_by_id('navWateringStations')).click()
        wait_for(lambda: self.driver.find_element_by_id(f'navWateringStation{ws_num}')).click()
