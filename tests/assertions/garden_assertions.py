from datetime import datetime, timedelta

import pytz
from garden.models import Garden


def assert_garden_connection_fields_are_updated(garden: Garden, response: str) -> None:
    assert garden.is_connected == True
    assert garden.last_connection_ip == response.wsgi_request.META.get('REMOTE_ADDR')
    assert datetime.now(pytz.UTC) - garden.last_connection_time < timedelta(seconds=1)
