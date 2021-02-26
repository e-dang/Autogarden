from selenium.webdriver import ActionChains

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

    def __set__(self, instance, value):
        element = self._get_element(instance)
        while self.__get__(instance, instance) != value:
            ActionChains(instance.driver).move_to_element(element).click().perform()

    def __get__(self, instance, owner):
        return self._get_element(instance).is_selected()

    def _get_element(self, instance):
        return wait_for(lambda: instance.driver.find_element_by_id(self.LOCATOR))


class Button:
    LOCATOR = None

    def __init__(self, instance):
        self.instance = instance

    def click(self):
        self._get_element().click()

    def _get_element(self):
        return wait_for(lambda: self.instance.driver.find_element_by_id(self.LOCATOR))
