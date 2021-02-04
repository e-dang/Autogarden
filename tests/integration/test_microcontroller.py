import pytest
from rest_framework.reverse import reverse


@pytest.mark.integration
class TestViews:
    def test_api_create_micro_controller_view_has_correct_url(self):
        assert reverse('api-create-micro-controller') == '/api/micro-controller/'
