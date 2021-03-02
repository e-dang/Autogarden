from unittest.mock import MagicMock, patch

import pytest
from users.managers import UserManager


@pytest.mark.unit
class TestUserManager:
    @pytest.mark.parametrize('is_staff, is_superuser, expected_is_staff, expected_is_superuser', [
        (None, None, False, False),
        (False, False, False, False),
        (True, True, True, True),
    ],
        ids=['None', 'False', 'True'])
    @patch.object(UserManager, '_create_user', MagicMock())
    def test_create_user_uses_user_values_or_sets_defaults_for_is_staff_and_is_superuser_if_not_defined(self, is_staff, is_superuser, expected_is_staff, expected_is_superuser):
        manager = UserManager()
        email = 'email@demo.com'
        password = 'random-test-password'
        kwargs = {}
        if is_staff is not None:
            kwargs['is_staff'] = is_staff
        if is_superuser is not None:
            kwargs['is_superuser'] = is_superuser

        manager.create_user(email, password, **kwargs)

        manager._create_user.assert_called_with(
            email, password, is_staff=expected_is_staff, is_superuser=expected_is_superuser
        )

    @patch.object(UserManager, '_create_user', MagicMock())
    def test_create_superuser_sets_is_staff_and_is_superuser_to_true_if_not_defined(self):
        manager = UserManager()
        email = 'email@demo.com'
        password = 'random-test-password'

        manager.create_superuser(email, password)

        manager._create_user.assert_called_with(email, password, is_staff=True, is_superuser=True)

    @pytest.mark.parametrize('is_staff, is_superuser', [
        (True, False),
        (False, True),
        (False, False),
    ],
        ids=['TF', 'FT', 'FF'])
    @patch.object(UserManager, '_create_user', MagicMock())
    def test_create_superuser_raises_an_error_if_is_staff_or_is_superuser_is_not_true(self, is_staff, is_superuser):
        manager = UserManager()
        email = 'email@demo.com'
        password = 'random-test-password'
        kwargs = {
            'is_staff': is_staff,
            'is_superuser': is_superuser
        }

        with pytest.raises(ValueError):
            manager.create_superuser(email, password, **kwargs)

    @patch.object(UserManager, 'normalize_email', MagicMock())
    def test_create_user_raises_value_error_if_normalized_email_is_empty_string(self):
        manager = UserManager()
        manager.normalize_email.return_value = ''
        email = 'email@demo.com'
        password = 'random-test-password'

        with pytest.raises(ValueError):
            manager._create_user(email, password)
