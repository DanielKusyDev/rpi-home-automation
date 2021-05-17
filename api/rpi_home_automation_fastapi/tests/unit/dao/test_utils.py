from enum import Enum

import pytest
from app.dao import utils


class _StabEnum(Enum):
    THING_ONE = "thing_one"


@pytest.mark.parametrize(
    "string, expected_string",
    [
        ("", ""),
        ("teststring", "teststring"),
        ("testString", "test_string"),
        ("testString123", "test_string_123"),
        ("TestString", "test_string"),
        ("TestString123", "test_string_123"),
        ("TestString123Test", "test_string_123_test"),
    ],
)
def test_to_snake_case(string, expected_string):
    assert utils.to_snake_case(string) == expected_string


@pytest.mark.parametrize(
    "row, to_snake, expected_result",
    [
        ({"Name": "fake_name"}, True, {"name": "fake_name"}),
        ({"Name": "fake_name"}, False, {"Name": "fake_name"}),
        ({"Age": 1}, True, {"age": 1}),
        ({"Enum": _StabEnum.THING_ONE}, True, {"enum": "thing_one"}),
    ],
)
def test_row_proxy_to_dict(row, to_snake, expected_result):
    assert utils.row_proxy_to_dict(row, to_snake) == expected_result
