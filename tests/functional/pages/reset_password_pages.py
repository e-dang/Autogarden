import re

from .base_page import BasePage
from .elements import Button, SubmitButton, TextInput


class PasswordField(TextInput):
    LOCATOR = 'id_new_password1'


class ConfirmPasswordField(TextInput):
    LOCATOR = 'id_new_password2'


class EmailInput(TextInput):
    LOCATOR = 'id_email'


class LoginButton(Button):
    LOCATOR = 'Log In'
    BY = 'find_element_by_link_text'


class ResetPasswordPage(BasePage):
    email = EmailInput()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)

    def has_correct_url(self):
        pattern = r'/reset_password/$'
        return re.search(pattern, self.driver.current_url) is not None


class ResetPasswordSentPage(BasePage):

    def has_correct_url(self):
        pattern = r'/reset_password_sent/$'
        return re.search(pattern, self.driver.current_url) is not None


class PasswordResetConfirmPage(BasePage):
    password = PasswordField()
    confirm_password = ConfirmPasswordField()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)

    def has_correct_url(self):
        pattern = r'/reset/.+/.+/$'
        return re.search(pattern, self.driver.current_url) is not None


class PasswordResetCompletePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.login_button = LoginButton(self)

    def has_correct_url(self):
        pattern = r'/reset_password_complete/$'
        return re.search(pattern, self.driver.current_url) is not None
