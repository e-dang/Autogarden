import re
import pytest
from django.urls import reverse

from .base import Base
from .pages.garden_list_page import GardenListPage
from .pages.login_page import LoginPage
from .pages.register_page import RegisterPage
from .pages.reset_password_pages import ResetPasswordPage, ResetPasswordSentPage, PasswordResetConfirmPage, PasswordResetCompletePage


class TestAuth(Base):
    @pytest.fixture(autouse=True)
    def init_server(self, live_server):
        self.live_server = live_server
        self.url = live_server.url + reverse('garden-list')

    @pytest.mark.django_db
    def test_user_can_create_account_and_login(self, test_password, mailoutbox):
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
        self.assert_user_is_logged_in(first_name)

        # the user clicks the logout button and is taken back to the login page
        garden_page.logout_button.click()
        self.wait_for_page_to_be_loaded(login_page)
        self.assert_user_is_logged_out(first_name)

        # the user has already forgotten their login information so they click the reset password link
        login_page.reset_password_button.click()
        reset_password_page = ResetPasswordPage(self.driver)
        self.wait_for_page_to_be_loaded(reset_password_page)

        # they enter their email address and click reset password
        reset_password_page.email = email
        reset_password_page.submit_button.click()

        # they are taken to the reset password sent page confirming that the email has been sent
        reset_password_sent_page = ResetPasswordSentPage(self.driver)
        self.wait_for_page_to_be_loaded(reset_password_sent_page)

        # they check their mail to get link to reset their password and find that the link has been sent.
        message = mailoutbox[0]
        assert message.to == [email]
        assert f'Password reset on' in message.subject
        url_search = re.search(r'http://.+/.+/', message.body)
        assert url_search is not None

        # they follow the link and are sent to the reset password confirm page
        self.driver.get(url_search.group(0))
        password_reset_confirm_page = PasswordResetConfirmPage(self.driver)
        self.wait_for_page_to_be_loaded(password_reset_confirm_page)

        # they now enter their new password and they are logged in and redirected back to the reset password
        # complete page
        new_password = 'my-new-string-test-password123'
        password_reset_confirm_page.password = new_password
        password_reset_confirm_page.confirm_password = new_password
        password_reset_confirm_page.submit_button.click()
        password_reset_complete_page = PasswordResetCompletePage(self.driver)
        self.wait_for_page_to_be_loaded(password_reset_complete_page)

        # they click the link to go to the login page
        password_reset_complete_page.login_button.click()

        # they now login with their new password and are taken to the garden list page
        login_page.email = email
        login_page.password = new_password
        login_page.submit_button.click()
        self.wait_for_page_to_be_loaded(garden_page)
