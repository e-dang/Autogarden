import re


class GardenDetailPage:
    def __init__(self, driver):
        self.driver = driver

    def has_correct_url(self):
        pattern = r'/gardens/[0-9]+/$'
        return re.search(pattern, self.driver.current_url) is not None

    def get_number_watering_stations(self):
        return len(self.driver.find_elements_by_css_selector('button[id*=wateringStationBtn]'))
