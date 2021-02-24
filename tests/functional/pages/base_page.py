class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click_home(self):
        self.driver.find_element_by_id('navBarHome').click()
