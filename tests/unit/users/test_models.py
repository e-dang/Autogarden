import pytest


@pytest.mark.unit
class TestUserModel:
    def test__str__returns_first_name_last_name_email(self, user_factory):
        user = user_factory.build()

        ret_val = user.__str__()

        assert user.email in ret_val
        assert user.first_name in ret_val
        assert user.last_name in ret_val
