import re

from .base_page import BasePage
from .elements import Button, SubmitButton, TextInput


class EmailField(TextInput):
    LOCATOR = 'id_email'


class PasswordField(TextInput):
    LOCATOR = 'id_password'


class RegisterButton(Button):
    LOCATOR = 'Sign Up'
    BY = 'find_element_by_link_text'


class ResetPasswordButton(Button):
    LOCATOR = 'Reset Password'
    BY = 'find_element_by_link_text'


class LoginPage(BasePage):
    email = EmailField()
    password = PasswordField()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self)
        self.register_button = RegisterButton(self)
        self.reset_password_button = ResetPasswordButton(self)

    def has_correct_url(self):
        pattern = r'/login/(\?next=[A-Za-z/-]+)*$'
        return re.search(pattern, self.driver.current_url) is not None

    def login(self, email, password):
        self.email = email
        self.password = password
        self.submit_button.click()
