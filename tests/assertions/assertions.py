from datetime import timedelta
from typing import Any, Dict, Iterable

from django.db.models import Model


def assert_image_files_equal(image_path1: str, image_path2: str) -> None:
    assert image_path1.split('/')[-1] == image_path2.split('/')[-1]


def assert_unordered_data_eq(data: Iterable[Any], expected_fields: Iterable[Any]) -> None:
    assert set(data) == set(expected_fields)


def assert_model_fields_have_values(data: Dict, model: Model) -> None:
    for field, value in data.items():
        assert getattr(model, field) == value


def assert_durations_are_eq(duration1: timedelta, duration2: timedelta, max_delta: timedelta = timedelta(seconds=1)) -> None:
    assert abs(duration1 - duration2) < max_delta
