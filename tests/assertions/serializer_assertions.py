from typing import List

import pytest
from rest_framework.exceptions import ErrorDetail


def assert_serializer_required_field_error(errors: List[ErrorDetail]) -> None:
    for err in errors:
        if err.code == 'required':
            return

    pytest.fail('Required error not found in list of errors')
