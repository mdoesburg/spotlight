from typing import Pattern, AnyStr, Any

from . import config
from .exceptions import FieldValueNotFoundError


def regex_match(compiled_regex: Pattern[AnyStr], value: Any) -> bool:
    """Checks if the value is a full match of the compiled regex"""
    try:
        match = compiled_regex.fullmatch(value)
    except:
        return False
    else:
        return match is not None


def equal(*values: Any) -> bool:
    """Checks if passed values are equal"""
    return len(set([str(v) for v in values])) == 1


def missing(data, field) -> bool:
    """Checks if the field is missing from data"""
    try:
        _get_field_value(data, field)
    except FieldValueNotFoundError:
        return True

    return False


def get_field_value(data, field) -> Any:
    """Return the value of the field in the data"""
    try:
        return _get_field_value(data, field)
    except FieldValueNotFoundError:
        return None


def _get_field_value(value, field):
    segments = field.split(config.FIELD_DELIMITER)
    try:
        for key in segments:
            if not isinstance(value, dict) and not isinstance(value, list):
                value = value.__dict__
            if key.isnumeric():
                value = value[int(key)]
            else:
                value = value[key]
    except (TypeError, AttributeError, KeyError, IndexError):
        raise FieldValueNotFoundError

    return value


def empty(value) -> bool:
    """Checks if the value is empty"""

    # Value is None
    if value is None:
        return True

    # Empty string
    if isinstance(value, str):
        if value.strip() == "":
            return True

    # Empty list or empty dict
    if isinstance(value, list) or isinstance(value, dict):
        if len(value) == 0:
            return True

    return False


def missing_or_empty(data, field) -> bool:
    value = get_field_value(data, field)

    return missing(data, field) or empty(value)
