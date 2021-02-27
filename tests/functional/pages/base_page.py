from .elements import Button


class HomeButton(Button):
    LOCATOR = 'navBarHome'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.home_button = HomeButton(self)
