import re

from .base_page import BasePage
from .elements import Button, TextInput


class EmailField(TextInput):
    LOCATOR = 'id_email'


class FirstNameField(TextInput):
    LOCATOR = 'id_first_name'


class LastNameField(TextInput):
    LOCATOR = 'id_last_name'


class PasswordField(TextInput):
    LOCATOR = 'id_password1'


class ConfirmPasswordField(TextInput):
    LOCATOR = 'id_password2'


class SubmitButton(Button):
    LOCATOR = 'submitBtn'


class RegisterPage(BasePage):
    email = EmailField()
    first_name = FirstNameField()
    last_name = LastNameField()
    password = PasswordField()
    confirm_password = ConfirmPasswordField()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)

    def has_correct_url(self):
        pattern = r'/register/$'
        return re.search(pattern, self.driver.current_url) is not None
