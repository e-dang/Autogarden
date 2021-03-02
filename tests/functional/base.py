import time

import pytest
from selenium.common.exceptions import WebDriverException

TIMEOUT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > TIMEOUT:
                    raise e
                time.sleep(0.5)

    return modified_fn


@wait
def wait_for(fn):
    return fn()


def wait_for_true(fn):
    start_time = time.time()
    while not wait_for(fn):
        if time.time() - start_time > TIMEOUT:
            raise WebDriverException('Function never evaluated to True')


@pytest.mark.functional
@pytest.mark.usefixtures('driver_init')
class Base:
    BOOSTRAP_MODAL_TOGGLE_DELAY = 0.5

    @wait
    def wait_for_page_to_be_loaded(self, page):
        assert page.has_correct_url()

    def wait_for_modal_to_be_visible(self, modal_id):
        wait_for_true(lambda: self.driver.find_element_by_id(modal_id).is_displayed())
        time.sleep(self.BOOSTRAP_MODAL_TOGGLE_DELAY)

    def wait_for_model_to_disappear(self, modal_id):
        wait_for_true(lambda: not self.driver.find_element_by_id(modal_id).is_displayed())
        time.sleep(self.BOOSTRAP_MODAL_TOGGLE_DELAY)

    def perform_image_crop(self, page, image):
        # the user selects an image, then crops it
        page.garden_image = image
        page.crop_image_button.click()

        # they see the crop button turn into a reset button and they click it
        page.reset_image_button.click()

        # they then see the reset button turn back to a crop button which they click again
        page.crop_image_button.click()
