import re

from garden.forms import CropperMixin, WateringStationForm

from ..base import wait_for
from .base_page import BasePage
from .elements import Button, CancelButton, DeleteButton, ImageInput, TextInput, ToggleButton, SubmitButton, ConfirmDeleteButton


class MoistureThresholdInput(TextInput):
    LOCATOR = 'id_moisture_threshold'


class WateringDurationInput(TextInput):
    LOCATOR = 'id_watering_duration'


class PlantTypeInput(TextInput):
    LOCATOR = 'id_plant_type'


class StatusCheckBox(ToggleButton):
    LOCATOR = 'id_status'


class WateringStationImage(ImageInput):
    INPUT_LOCATOR = 'id_image'
    IMAGE_LOCATOR = 'wateringStationImage'


class CropButton(Button):
    LOCATOR = CropperMixin.CROP_BTN_ID


class ResetButton(Button):
    LOCATOR = CropperMixin.RESET_BTN_ID


class WateringStationUpdatePage(BasePage):
    moisture_threshold = MoistureThresholdInput()
    watering_duration = WateringDurationInput()
    plant_type = PlantTypeInput()
    status = StatusCheckBox()
    image = WateringStationImage()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)
        self.delete_button = DeleteButton(self)
        self.cancel_button = CancelButton(self)
        self.confirm_delete_button = ConfirmDeleteButton(self)
        self.crop_image_button = CropButton(self)
        self.reset_image_button = ResetButton(self)
        self.modal_id = WateringStationForm.MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/watering-stations/[0-9]+/update/$'
        return re.search(pattern, self.driver.current_url) is not None

    def go_to_watering_station_page(self, ws_num):
        wait_for(lambda: self.driver.find_element_by_id('navWateringStations')).click()
        wait_for(lambda: self.driver.find_element_by_id(f'navWateringStation{ws_num}')).click()

    def update_info(self, status=None, plant_type=None, moisture_threshold=None, watering_duration=None, image=None, crop_image=lambda x, y: None):
        if status is not None:
            self.status = status
        if plant_type is not None:
            self.plant_type = plant_type
        if moisture_threshold is not None:
            self.moisture_threshold = moisture_threshold
        if watering_duration is not None:
            self.watering_duration = watering_duration
        if image is not None:
            self.image = image
            crop_image(self, image)
        self.submit_button.click()
