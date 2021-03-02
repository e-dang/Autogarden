import re

from users.forms import LoginForm

from .base_page import BasePage
from .elements import Button


class RegisterButton(Button):
    LOCATOR = LoginForm.REGISTER_BTN_ID


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.register_button = RegisterButton(self)

    def has_correct_url(self):
        pattern = r'/login/(\?next=[A-Za-z/-]+)*$'
        return re.search(pattern, self.driver.current_url) is not None
