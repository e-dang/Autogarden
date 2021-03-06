from typing import Dict, Iterable

from django.db.models import Model


def assert_image_files_equal(image_path1: str, image_path2: str) -> None:
    assert image_path1.split('/')[-1] == image_path2.split('/')[-1]


def assert_data_contains_fields(data: Dict, expected_fields: Iterable[str]) -> None:
    assert set(data) == set(expected_fields)


def assert_model_fields_have_values(data: Dict, model: Model) -> None:
    for field, value in data.items():
        assert getattr(model, field) == value
