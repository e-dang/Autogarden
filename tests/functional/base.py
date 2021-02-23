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


@pytest.mark.functional
@pytest.mark.usefixtures('driver_init')
class Base:
    @wait
    def wait_for_page_to_be_loaded(self, page):
        assert page.has_correct_url()
