import pytest

from .base import Base
from .pages.garden_list_page import GardenListPage
from .pages.login_page import LoginPage
from .pages.settings_page import SettingsPage
from .pages.change_password_page import ChangePasswordPage, ChangePasswordDonePage
from django.urls import reverse


class TestChangeUserSettings(Base):
    @pytest.fixture(autouse=True)
    def setup(self, create_user, live_server):
        self.email = 'email@demo.com'
        self.url = live_server.url + reverse('garden-list')
        self.user = create_user(email=self.email)
        self.create_authenticated_session(self.user, live_server)

    def test_user_can_change_their_settings(self, test_password):
        # a logged in user is at their garden list page
        self.driver.get(self.url)
        list_gpage = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(list_gpage)

        # they see a button in the navbar that allows them to change their settings. They click it.
        list_gpage.settings_button.click()
        settings_page = SettingsPage(self.driver)
        self.wait_for_page_to_be_loaded(settings_page)

        # the user sees a form allowing them to change some fields like email, but not the password field. They decide
        # to alter these fields.
        first_name = self.user.first_name + 'extra_chars'
        last_name = self.user.last_name + 'extra_chars'
        email = self.user.email + 'extrachars'
        settings_page.submit_info(first_name, last_name, email)

        # the user sees that the form now has their current info as well as the welcome message in the navbar which
        # now displays their new name
        assert settings_page.info_is_equal(first_name, last_name, email)
        self.assert_user_is_logged_in(first_name)

        # the user also sees a button that allows them to change their password and so they click it. They are brought
        # to the change password page
        settings_page.change_password_button.click()
        change_password_page = ChangePasswordPage(self.driver)
        self.wait_for_page_to_be_loaded(change_password_page)

        # the user enters info to change their password and submits it
        new_password = '18jugdbsdgl[-aqdfp'
        change_password_page.change_password(test_password, new_password)

        # the user is now taken to the change_password_done page. They want to see if their password really changed, so
        # they logout and try to log back in. It is successful.
        change_password_done_page = ChangePasswordDonePage(self.driver)
        self.wait_for_page_to_be_loaded(change_password_done_page)
        change_password_done_page.logout_button.click()

        login_page = LoginPage(self.driver)
        self.wait_for_page_to_be_loaded(login_page)
        login_page.login(email, new_password)

        self.wait_for_page_to_be_loaded(list_gpage)
