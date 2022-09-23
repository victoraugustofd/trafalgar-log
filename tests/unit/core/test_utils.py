import logging
from dataclasses import dataclass
from typing import NoReturn, Optional

from trafalgar_log.app import SETTINGS
from trafalgar_log.core.utils import (
    initialize_logger,
    get_payload,
    CustomJsonFormatter,
)


def test_initialize_logger() -> NoReturn:
    logger = initialize_logger()

    assert logger.name == SETTINGS.get("APP_NAME")
    assert logging.getLevelName(logger.level) == SETTINGS.get("HAKI")
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0].formatter, CustomJsonFormatter)


def test_get_payload() -> NoReturn:
    int_payload = 1
    float_payload = 1.1
    str_payload = "testing"
    bool_payload = True
    list_payload = ["a", "b", 1]
    dict_payload = {"a": 1, "b": 2, "c": "1"}
    tuple_payload = ("a", "b", 1)
    complex_payload = TestComplexObjectWithDataClass("1", "2", "3")
    complex_payload2 = TestComplexObjectWithoutDataClass("1", "2", "3")
    complex_payload3 = TestComplexObjectWithDataClass(
        "1", "2", "3", TestComplexObjectWithoutDataClass(1, 1.1, True)
    )

    assert get_payload(int_payload) == 1
    assert get_payload(float_payload) == 1.1
    assert get_payload(str_payload) == "testing"
    assert get_payload(bool_payload) is True
    assert get_payload(not bool_payload) is False
    assert get_payload(list_payload) == ["a", "b", 1]
    assert get_payload(dict_payload) == {"a": 1, "b": 2, "c": "1"}
    assert get_payload(tuple_payload) == ["a", "b", 1]
    assert get_payload(complex_payload) == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": None,
    }
    assert get_payload(complex_payload2) == {"a": "1", "b": "2", "c": "3"}
    assert get_payload(complex_payload3) == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": {"a": 1, "b": 1.1, "c": True},
    }


def test_get_masked_payload() -> NoReturn:
    complex_payload = TestMaskComplexObjectWithoutDataClass("1", "2", "3")
    complex_payload2 = TestMaskComplexObjectWithDataClass(
        "1", "2", "3", TestMaskComplexObjectWithoutDataClass(1, 1.1, True)
    )

    assert get_payload(complex_payload) == {"a": "1", "b": "2", "mask": "*"}
    assert get_payload(complex_payload2) == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": {"a": 1, "b": 1.1, "mask": "*"},
    }


class TestComplexObjectWithoutDataClass(object):
    a: object
    b: object
    c: object

    def __init__(self, a: object, b: object, c: object):
        self.a = a
        self.b = b
        self.c = c


@dataclass
class TestComplexObjectWithDataClass(object):
    a: object
    b: object
    c: object
    d: Optional[TestComplexObjectWithoutDataClass] = None


class TestMaskComplexObjectWithoutDataClass(object):
    a: object
    b: object
    mask: object

    def __init__(self, a: object, b: object, mask: object):
        self.a = a
        self.b = b
        self.mask = mask


@dataclass
class TestMaskComplexObjectWithDataClass(object):
    a: object
    b: object
    c: object
    d: Optional[TestMaskComplexObjectWithoutDataClass] = None
