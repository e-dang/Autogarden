import re
from tests.functional.pages.elements import Button, TextInput

from .base_page import BasePage


class FirstNameInput(TextInput):
    LOCATOR = 'id_first_name'


class LastNameInput(TextInput):
    LOCATOR = 'id_last_name'


class EmailInput(TextInput):
    LOCATOR = 'id_email'


class SubmitButton(Button):
    LOCATOR = '//input[@type="submit"]'


class ChangePasswordButton(Button):
    LOCATOR = 'changePasswordBtn'


class SettingsPage(BasePage):
    first_name = FirstNameInput()
    last_name = LastNameInput()
    email = EmailInput()

    def __init__(self, driver):
        super().__init__(driver)
        self.submit_button = SubmitButton(self, 'find_element_by_xpath')
        self.change_password_button = ChangePasswordButton(self)

    def has_correct_url(self):
        pattern = r'/settings/$'
        return re.search(pattern, self.driver.current_url) is not None

    def submit_info(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.submit_button.click()

    def info_is_equal(self, first_name, last_name, email):
        return all([self.first_name == first_name,
                    self.last_name == last_name,
                    self.email == email])
