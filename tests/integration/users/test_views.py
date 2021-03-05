import pytest
from django.urls import reverse
from tests.assertions import assert_redirect, assert_template_is_rendered

from users.models import User


@pytest.fixture
def signup_info(user_factory, test_password):
    return user_factory.signup_info(password=test_password)


@pytest.mark.integration
class TestLoginView:
    @pytest.fixture(autouse=True)
    def create_url(self):
        self.url = reverse('login')

    def test_view_has_correct_url(self):
        assert self.url == '/login/'

    def test_GET_renders_login_html(self, client):
        resp = client.get(self.url)

        assert_template_is_rendered(resp, 'login.html')

    @pytest.mark.django_db
    def test_POST_with_valid_credentials_logs_user_in(self, client, create_user, test_password):
        user = create_user()
        data = {
            'email': user.email,
            'password': test_password
        }

        client.post(self.url, data=data)

        assert client.session.get('_auth_user_id') == str(user.pk)

    @pytest.mark.django_db
    def test_POST_with_valid_credentials_redirects_to_garden_list_view(self, client, create_user, test_password):
        user = create_user()
        data = {
            'email': user.email,
            'password': test_password
        }

        resp = client.post(self.url, data=data)

        assert_redirect(resp, reverse('garden-list'))

    @pytest.mark.django_db
    def test_POST_with_invalid_credentials_renders_login_html(self, client, user, test_password):
        data = {
            'email': user.email,
            'password': test_password + 'extra-chars'
        }

        resp = client.post(self.url, data=data)

        assert_template_is_rendered(resp, 'login.html')

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'post'], ids=['get', 'post'])
    def test_requests_from_already_logged_in_user_redirects_to_garden_list_page(self, auth_client, method):
        resp = getattr(auth_client, method)(self.url)

        assert_redirect(resp, reverse('garden-list'))


@pytest.mark.integration
class TestLogoutView:
    @pytest.fixture(autouse=True)
    def create_url(self):
        self.url = reverse('logout')

    def test_view_has_correct_url(self):
        assert self.url == '/logout/'

    @pytest.mark.django_db
    def test_GET_logs_out_the_logged_in_user(self, true_auth_client):
        resp = true_auth_client.get(self.url)

        assert not resp.wsgi_request.user.is_authenticated
        assert '_auth_user_id' not in true_auth_client.session

    @pytest.mark.django_db
    def test_GET_redirects_to_login_view(self, true_auth_client):
        resp = true_auth_client.get(self.url)

        assert_redirect(resp, reverse('login'))


@pytest.mark.integration
class TestCreateUserView:
    @pytest.fixture(autouse=True)
    def create_url(self):
        self.url = reverse('register')

    def test_view_has_correct_url(self):
        assert self.url == '/register/'

    def test_GET_renders_register_html(self, client):
        resp = client.get(self.url)

        assert_template_is_rendered(resp, 'register.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_a_new_user_with_provided_credentials(self, client, signup_info):
        client.post(self.url, data=signup_info)

        assert User.objects.get(
            email=signup_info['email'],
            first_name=signup_info['first_name'],
            last_name=signup_info['last_name']
        )

    @pytest.mark.django_db
    def test_POST_with_valid_data_logs_in_the_created_user(self, client, signup_info):
        client.post(self.url, data=signup_info)

        assert client.session['_auth_user_id'] == str(User.objects.get(email=signup_info['email']).pk)

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_list_view(self, client, signup_info):
        resp = client.post(self.url, data=signup_info)

        assert_redirect(resp, reverse('garden-list'))


@pytest.mark.integration
class TestSettingsView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = reverse('settings')

    @pytest.mark.django_db
    def test_GET_renders_settings_html(self, auth_client):
        resp = auth_client.get(self.url)

        assert_template_is_rendered(resp, 'settings.html')

    @pytest.mark.django_db
    def test_POST_updates_user_with_posted_data(self, auth_client, auth_user):
        data = {
            'first_name': auth_user.first_name + 'extra_chars',
            'last_name': auth_user.last_name + 'extra_chars',
            'email': 'extra_chars' + auth_user.email
        }

        auth_client.post(self.url, data=data)

        auth_user.refresh_from_db()
        assert auth_user.first_name == data['first_name']
        assert auth_user.last_name == data['last_name']
        assert auth_user.email == data['email']

    @pytest.mark.django_db
    def test_POST_with_valid_data_redirects_to_settings(self, auth_client, auth_user):
        data = {
            'first_name': auth_user.first_name + 'extra_chars',
            'last_name': auth_user.last_name + 'extra_chars',
            'email': 'extra_chars' + auth_user.email
        }

        resp = auth_client.post(self.url, data=data)

        assert_redirect(resp, reverse('settings'))

    @pytest.mark.django_db
    def test_POST_with_invalid_data_renders_settings_html_with_errors(self, auth_client):
        invalid_data = {}

        resp = auth_client.post(self.url, data=invalid_data)

        assert_template_is_rendered(resp, 'settings.html')
        assert 'This field is required' in str(resp.content)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'post'], ids=['get', 'post'])
    def test_view_redirects_to_login_page_if_accessed_by_non_logged_in_user(self, client, method):
        resp = getattr(client, method)(self.url)

        assert_redirect(resp, reverse('login'), self.url)
