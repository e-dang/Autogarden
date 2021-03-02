import pytest
from django.urls import reverse

from .base import Base
from .pages.garden_list_page import GardenListPage
from .pages.login_page import LoginPage
from .pages.register_page import RegisterPage


class TestAuth(Base):
    @pytest.fixture(autouse=True)
    def init_server(self, live_server):
        self.url = live_server.url + reverse('garden-list')

    @pytest.mark.django_db
    def test_user_can_create_account_and_login(self, test_password):
        # a user goes tries to go to the homepage but is redirected to the login page
        self.driver.get(self.url)
        login_page = LoginPage(self.driver)
        self.wait_for_page_to_be_loaded(login_page)

        # the user does not have an account so they click the register button
        login_page.register_button.click()
        register_page = RegisterPage(self.driver)

        # they are taken to the register page where they type in their information and submit it
        email = 'demo@email.com'
        first_name = 'test'
        last_name = 'user'
        register_page.email = email
        register_page.first_name = first_name
        register_page.last_name = last_name
        register_page.password = test_password
        register_page.confirm_password = test_password
        register_page.submit_button.click()

        # after successful registration the user is redirected to the home page
        garden_page = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(garden_page)

        # the user sees their name and a logout button in the navbar indicating that they are logged in
        assert False, 'Finish the test!'

        # the user clicks the logout button and is taken back to the login page

        # the user has already forgotten their login information so they click the forgot password link

        # they enter their email address and click reset password

        # they reset their password and are again redirected to the login page

        # they now enter their new password and they are logged in and redirected back to the home page
