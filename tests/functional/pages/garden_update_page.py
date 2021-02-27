import re

from garden.forms import DeleteGardenForm, UpdateGardenForm

from .base_page import BasePage
from .elements import Button, TextInput


class GardenNameInput(TextInput):
    LOCATOR = 'id_name'


class GardenImageInput(TextInput):
    LOCATOR = 'id_image'


class SubmitButton(Button):
    LOCATOR = UpdateGardenForm.SUBMIT_BTN_ID


class DeleteButton(Button):
    LOCATOR = UpdateGardenForm.DELETE_BTN_ID


class ConfirmDeleteButton(Button):
    LOCATOR = DeleteGardenForm.CONFIRM_DELETE_BTN_ID


class CancelDeleteButton(Button):
    LOCATOR = DeleteGardenForm.CANCEL_DELETE_BTN_ID


class GardenUpdatePage(BasePage):
    garden_name = GardenNameInput()
    garden_image = GardenImageInput()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)
        self.delete_button = DeleteButton(self)
        self.confirm_delete_button = ConfirmDeleteButton(self)
        self.cancel_delete_button = CancelDeleteButton(self)
        self.modal_id = UpdateGardenForm.DELETE_GARDEN_MODAL_ID

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/update/$'
        return re.search(pattern, self.driver.current_url) is not None
