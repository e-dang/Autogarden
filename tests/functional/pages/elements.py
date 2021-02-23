from ..base import wait_for


class TextInput:
    LOCATOR = None

    def __set__(self, obj, value):
        element = wait_for(lambda: obj.driver.find_element_by_id(self.LOCATOR))
        element.clear()
        element.send_keys(value)

    def __get__(self, obj, owner):
        return wait_for(lambda: obj.driver.find_element_by_id(self.LOCATOR)).get_attribute('value')
