import re

from .base_page import BasePage


class UnauthorizedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def has_correct_url(self):
        pattern = r'/unauthorized/$'
        return re.search(pattern, self.driver.current_url) is not None
