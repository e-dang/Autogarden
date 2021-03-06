import re
from tests.assertions.assertions import assert_image_files_equal

import pytest

from garden.forms import UpdateGardenForm

from .base_page import BasePage
from .elements import Button, CancelButton, ConfirmDeleteButton, DeleteButton, SubmitButton, TextInput, ImageInput


class GardenNameInput(TextInput):
    LOCATOR = 'id_name'


class GardenImageInput(ImageInput):
    INPUT_LOCATOR = 'id_image'
    IMAGE_LOCATOR = 'gardenImage'


class UpdateInterval(TextInput):
    LOCATOR = 'id_update_interval'


class CropButton(Button):
    LOCATOR = UpdateGardenForm.CROP_BTN_ID


class ResetButton(Button):
    LOCATOR = UpdateGardenForm.RESET_BTN_ID


class GardenUpdatePage(BasePage):
    name = GardenNameInput()
    image = GardenImageInput()
    update_interval = UpdateInterval()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)
        self.delete_button = DeleteButton(self)
        self.confirm_delete_button = ConfirmDeleteButton(self)
        self.cancel_button = CancelButton(self)
        self.crop_image_button = CropButton(self)
        self.reset_image_button = ResetButton(self)
        self.modal_id = UpdateGardenForm.MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/update/$'
        return re.search(pattern, self.driver.current_url) is not None

    def update_garden(self, submit=True, **kwargs):
        for field, value in kwargs.items():
            if not hasattr(self, field):
                pytest.fail(f'GardenUpdatePage cannot set the value for {field} because that field doesnt exist')
            setattr(self, field, value)

        if submit:
            self.submit_button.click()

    def assert_form_has_values(self, **kwargs):
        for field, value in kwargs.items():
            if not hasattr(self, field):
                pytest.fail(f'GardenUpdatePage cannot check value for {field} because that field doesnt exist')

            if field == 'image':
                assert_image_files_equal(self.image, value)
            else:
                assert getattr(self, field) == value
