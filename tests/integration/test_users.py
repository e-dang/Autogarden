import pytest
from django.http import HttpRequest
from django.urls import reverse
from users.authentication import EmailBackend
from users.models import User

from .conftest import assert_redirect, assert_template_is_rendered


@pytest.fixture
def valid_user_info(test_password):
    return {
        'email': 'email@demo.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': test_password,
        'password2': test_password

    }


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

        assert client.session.get('_auth_user_id') == user.pk

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
    def test_POST_with_valid_data_creates_a_new_user_with_provided_credentials(self, client, valid_user_info):
        client.post(self.url, data=valid_user_info)

        assert User.objects.get(
            email=valid_user_info['email'],
            first_name=valid_user_info['first_name'],
            last_name=valid_user_info['last_name']
        )

    @pytest.mark.django_db
    def test_POST_with_valid_data_logs_in_the_created_user(self, client, valid_user_info):
        client.post(self.url, data=valid_user_info)

        assert client.session['_auth_user_id'] == User.objects.get(email=valid_user_info['email']).pk

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_list_view(self, client, valid_user_info):
        resp = client.post(self.url, data=valid_user_info)

        assert_redirect(resp, reverse('garden-list'))


@pytest.mark.integration
class TestEmailBackend:
    @pytest.mark.django_db
    def test_authenticate_returns_none_when_email_does_not_belong_to_any_user(self, create_user, test_password):
        request = HttpRequest()
        backend = EmailBackend()
        user = create_user()
        email = user.email + 'some_random_chars'

        ret_val = backend.authenticate(request, email=email, password=test_password)

        assert ret_val is None

    @pytest.mark.django_db
    def test_authenticate_returns_none_when_password_is_incorrect(self, create_user, test_password):
        request = HttpRequest()
        backend = EmailBackend()
        user = create_user()
        password = test_password + 'some_random_chars'

        ret_val = backend.authenticate(request, email=user.email, password=password)

        assert ret_val is None

    @pytest.mark.django_db
    def test_authenticate_returns_none_when_user_is_inactive(self, create_user, test_password):
        request = HttpRequest()
        backend = EmailBackend()
        user = create_user(is_active=False)

        ret_val = backend.authenticate(request, email=user.email, password=test_password)

        assert ret_val is None

    @pytest.mark.django_db
    def test_authenticate_returns_user_if_both_email_and_password_are_correct_and_user_is_active(self, create_user, test_password):
        request = HttpRequest()
        backend = EmailBackend()
        user = create_user(is_active=True)

        ret_val = backend.authenticate(request, email=user.email, password=test_password)

        assert ret_val == user

    @pytest.mark.django_db
    def test_get_user_returns_none_if_provided_id_does_not_match_any_users(self, create_user):
        user = create_user()
        backend = EmailBackend()

        ret_val = backend.get_user(user.pk + 'extra_chars')

        assert ret_val is None

    @pytest.mark.django_db
    def test_get_user_returns_none_if_specified_user_is_inactive(self, create_user):
        user = create_user(is_active=False)
        backend = EmailBackend()

        ret_val = backend.get_user(user.pk)

        assert ret_val is None

    @pytest.mark.django_db
    def test_get_user_returns_specified_user_when_user_is_active(self, create_user):
        user = create_user(is_active=True)
        backend = EmailBackend()

        ret_val = backend.get_user(user.pk)

        assert ret_val == user
