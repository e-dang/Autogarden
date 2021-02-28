from .elements import Button


class HomeButton(Button):
    LOCATOR = 'navBarHome'


class GardenDetailButton(Button):
    LOCATOR = 'navGardenDetail'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.home_button = HomeButton(self)
        self.garden_detail_nav_button = GardenDetailButton(self)
