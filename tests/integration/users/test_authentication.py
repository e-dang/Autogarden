import pytest
from django.http import HttpRequest

from users.authentication import EmailBackend


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

        ret_val = backend.get_user(user.pk + 1)

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
