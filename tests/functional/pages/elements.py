from ..base import wait_for


class TextInput:
    LOCATOR = None

    def __set__(self, obj, value):
        element = wait_for(lambda: obj.driver.find_element_by_id(self.LOCATOR))
        element.clear()
        element.send_keys(value)

    def __get__(self, obj, owner):
        return wait_for(lambda: obj.driver.find_element_by_id(self.LOCATOR)).get_attribute('value')


class ButtonGroup:
    LOCATOR = None
    element = None

    def __set__(self, instance, value):
        self.element = wait_for(lambda: instance.driver.find_element_by_id(self.LOCATOR + str(value)))
        self.element.click()

    def __get__(self, instance, owner):
        return self.element


class ToggleButton:
    LOCATOR = None
    element = None

    def __set__(self, instance, value):
        while self.__get__(instance, instance) != value:
            self.element.click()

    def __get__(self, instance, owner):
        if self.element is None:
            self._get_element(instance)
        return self.element.is_selected()

    def _get_element(self, instance):
        self.element = wait_for(lambda: instance.driver.find_element_by_id(self.LOCATOR))
