import re

from .base_page import BasePage
from .elements import TextInput, SubmitButton


class OldPasswordInput(TextInput):
    LOCATOR = 'id_old_password'


class PasswordInput(TextInput):
    LOCATOR = 'id_new_password1'


class ConfirmPasswordInput(TextInput):
    LOCATOR = 'id_new_password2'


class ChangePasswordPage(BasePage):
    old_password = OldPasswordInput()
    password = PasswordInput()
    confirm_password = ConfirmPasswordInput()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)

    def has_correct_url(self):
        pattern = r'/password_change/$'
        return re.search(pattern, self.driver.current_url) is not None

    def change_password(self, old_password, password):
        self.old_password = old_password
        self.password = password
        self.confirm_password = password
        self.submit_button.click()


class ChangePasswordDonePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def has_correct_url(self):
        pattern = r'/password_change_done/$'
        return re.search(pattern, self.driver.current_url) is not None
