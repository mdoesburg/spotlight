import ipaddress
import json
import re
from datetime import datetime
from decimal import Decimal
from json import JSONDecodeError
from typing import Any, Tuple, List
from uuid import UUID
from abc import ABC, abstractmethod

from . import errors, config
from .exceptions import (
    RuleNameAlreadyExistsError,
    AttributeNotImplementedError,
    InvalidDateTimeFormat,
)
from .utils import missing, equal, empty, regex_match, missing_or_empty, get_field_value


class Rule(ABC):
    name = NotImplemented
    implicit = False
    stop = False

    subclasses = []

    def __init__(self):
        self.message_fields = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.name is NotImplemented:
            raise AttributeNotImplementedError("name", cls.__name__)
        if cls.name in [subclass.name for subclass in cls.subclasses]:
            raise RuleNameAlreadyExistsError(cls.name)

        cls.subclasses.append(cls)

    @abstractmethod
    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        """
        Tests if the field that is being validated passes the rule.

        Parameters
        ----------
        field : str
            The name of the field that is being validated.
        value : Any
            The value of the field that is being validated.
        parameters : list
            A list of rule parameters.
        validator : Validator
            Instance of the validator. Can be used to access data and rules.
            Useful for more advanced rules that are dependent on other fields.

        Returns
        -------
        bool
            Returns a boolean that indicates if the field that is being
            validated passed the rule.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError


class RequiredRule(Rule):
    """Required field"""

    name = "required"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return not missing(validator.data, field) and not empty(value)

    @property
    def message(self) -> str:
        return errors.REQUIRED_ERROR


class RequiredWithoutRule(Rule):
    """Required if other field is not present"""

    name = "required_without"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        other_fields = parameters
        data = validator.data
        self.message_fields = dict(field=field, other=", ".join(other_fields))

        if missing_or_empty(data, field) and any(
            [missing_or_empty(data, o) for o in other_fields]
        ):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.REQUIRED_WITHOUT_ERROR


class RequiredWithRule(Rule):
    """Required with other field"""

    name = "required_with"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        other_fields = parameters
        data = validator.data
        self.message_fields = dict(field=field, other=", ".join(other_fields))

        if missing_or_empty(data, field) and any(
            [not missing_or_empty(data, o) for o in other_fields]
        ):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.REQUIRED_WITH_ERROR


class RequiredIfRule(Rule):
    """Required if other field equals certain value"""

    name = "required_if"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        other, val = parameters
        data = validator.data
        other_val = get_field_value(data=data, field=other)
        self.message_fields = dict(field=field, other=other, value=val)

        if missing_or_empty(data, field) and equal(val, other_val):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.REQUIRED_IF_ERROR


class RequiredUnlessRule(Rule):
    """Required unless other field equals certain value"""

    name = "required_unless"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        other, val = parameters
        data = validator.data
        other_val = get_field_value(data=data, field=other)
        self.message_fields = dict(field=field, other=other, value=val)

        if missing_or_empty(data, field) and not equal(val, other_val):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.REQUIRED_UNLESS_ERROR


class NotWithRule(Rule):
    """Not with other field"""

    name = "not_with"
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        other = parameters[0]
        data = validator.data
        self.message_fields = dict(field=field, other=other)

        if not missing(data, field) and not missing(data, other):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.NOT_WITH_ERROR


class FilledRule(Rule):
    """Not empty when present"""

    name = "filled"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        if not missing(validator.data, field) and empty(value):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.FILLED_ERROR


class EmailRule(Rule):
    """Valid email"""

    name = "email"
    _regex = re.compile(
        r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    )

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_email(value)

    @property
    def message(self) -> str:
        return errors.EMAIL_ERROR

    @staticmethod
    def valid_email(email) -> bool:
        return regex_match(EmailRule._regex, email)


class UrlRule(Rule):
    """Valid URL"""

    name = "url"
    _regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_url(value)

    @property
    def message(self) -> str:
        return errors.URL_ERROR

    @staticmethod
    def valid_url(url) -> bool:
        return regex_match(UrlRule._regex, url)


class IpRule(Rule):
    """Valid IP"""

    name = "ip"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_ip(value)

    @property
    def message(self) -> str:
        return errors.IP_ERROR

    @staticmethod
    def valid_ip(ip) -> bool:
        if not StringRule.valid_string(ip) and not IntegerRule.valid_integer(ip):
            return False

        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False


class MinRule(Rule):
    """Min length"""

    name = "min"

    def __init__(self):
        super().__init__()
        self.error = None

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        min_ = parameters[0]
        self.message_fields = dict(field=field, min=min_)
        self.error = errors.MIN_ERROR
        expected = float(min_)

        if isinstance(value, str):
            self.error = errors.MIN_STRING_ERROR
            return len(value) >= expected
        elif isinstance(value, list) or isinstance(value, dict):
            self.error = errors.MIN_ITEMS_ERROR
            return len(value) >= expected
        elif isinstance(value, int):
            return value >= expected
        elif isinstance(value, float):
            return value >= expected
        elif isinstance(value, Decimal):
            expected = Decimal(min_)
            return value >= expected

        return False

    @property
    def message(self) -> str:
        return self.error


class MaxRule(Rule):
    """Max length"""

    name = "max"

    def __init__(self):
        super().__init__()
        self.error = None

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        max_ = parameters[0]
        self.message_fields = dict(field=field, max=max_)
        self.error = errors.MAX_ERROR
        expected = float(max_)

        if isinstance(value, str):
            self.error = errors.MAX_STRING_ERROR
            return len(value) <= expected
        elif isinstance(value, list) or isinstance(value, dict):
            self.error = errors.MAX_ITEMS_ERROR
            return len(value) <= expected
        elif isinstance(value, int):
            return value <= expected
        elif isinstance(value, float):
            return value <= expected
        elif isinstance(value, Decimal):
            expected = Decimal(max_)
            return value <= expected

        return False

    @property
    def message(self) -> str:
        return self.error


class InRule(Rule):
    """
    In: The field under validation must be included in the given list of values
    """

    name = "in"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field, values=parameters)

        return str(value) in parameters

    @property
    def message(self) -> str:
        return errors.IN_ERROR


class AlphaNumRule(Rule):
    """Only letters and numbers"""

    name = "alpha_num"
    _regex = re.compile(r"^[a-zA-Z0-9]+$")

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num(value)

    @property
    def message(self) -> str:
        return errors.ALPHA_NUM_ERROR

    @staticmethod
    def valid_alpha_num(value) -> bool:
        return regex_match(AlphaNumRule._regex, value)


class AlphaNumSpaceRule(Rule):
    """Only letters, numbers and spaces"""

    name = "alpha_num_space"
    _regex = re.compile(r"^[a-zA-Z0-9 ]+$")

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num_space(value)

    @property
    def message(self) -> str:
        return errors.ALPHA_NUM_SPACE_ERROR

    @staticmethod
    def valid_alpha_num_space(value) -> bool:
        return regex_match(AlphaNumSpaceRule._regex, value)


class StringRule(Rule):
    """Valid string"""

    name = "string"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_string(value)

    @property
    def message(self) -> str:
        return errors.STRING_ERROR

    @staticmethod
    def valid_string(string) -> bool:
        return isinstance(string, str)


class IntegerRule(Rule):
    """Valid integer"""

    name = "integer"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_integer(value)

    @property
    def message(self) -> str:
        return errors.INTEGER_ERROR

    @staticmethod
    def valid_integer(integer) -> bool:
        return isinstance(integer, int)


class FloatRule(Rule):
    """Valid float"""

    name = "float"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_float(value)

    @property
    def message(self) -> str:
        return errors.FLOAT_ERROR

    @staticmethod
    def valid_float(float_) -> bool:
        return isinstance(float_, float)


class DecimalRule(Rule):
    """Valid decimal"""

    name = "decimal"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_decimal(value)

    @property
    def message(self) -> str:
        return errors.DECIMAL_ERROR

    @staticmethod
    def valid_decimal(value) -> bool:
        return isinstance(value, Decimal)


class BooleanRule(Rule):
    """Valid boolean"""

    name = "boolean"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_boolean(value)

    @property
    def message(self) -> str:
        return errors.BOOLEAN_ERROR

    @staticmethod
    def valid_boolean(boolean) -> bool:
        return isinstance(boolean, bool)


class ListRule(Rule):
    """Valid list"""

    name = "list"
    stop = True

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_list(value)

    @property
    def message(self) -> str:
        return errors.LIST_ERROR

    @staticmethod
    def valid_list(value) -> bool:
        return isinstance(value, list)


class Uuid4Rule(Rule):
    """Valid uuid4"""

    name = "uuid4"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_uuid4(value)

    @property
    def message(self) -> str:
        return errors.UUID4_ERROR

    @staticmethod
    def valid_uuid4(uuid) -> bool:
        if isinstance(uuid, UUID):
            uuid = str(uuid)
        try:
            val = UUID(uuid, version=4)
        except (TypeError, ValueError, AttributeError):
            return False

        return str(val) == uuid


class JsonRule(Rule):
    """Valid json"""

    name = "json"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_json(value)

    @property
    def message(self) -> str:
        return errors.JSON_ERROR

    @staticmethod
    def valid_json(value) -> bool:
        try:
            json.loads(value)
            return True
        except (TypeError, JSONDecodeError):
            return False


class AcceptedRule(Rule):
    """The field must be yes, on, 1, or true"""

    name = "accepted"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        accepted_values = ["yes", "on", 1, True]
        self.message_fields = dict(field=field)

        return value in accepted_values

    @property
    def message(self) -> str:
        return errors.ACCEPTED_ERROR


class StartsWithRule(Rule):
    """The field under validation must start with one of the given values."""

    name = "starts_with"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field, values=parameters)

        return any([str(value).startswith(rule_val) for rule_val in parameters])

    @property
    def message(self) -> str:
        return errors.STARTS_WITH_ERROR


class DictRule(Rule):
    """Valid dict"""

    name = "dict"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_dict(value)

    @property
    def message(self) -> str:
        return errors.DICT_ERROR

    @staticmethod
    def valid_dict(value) -> bool:
        return isinstance(value, dict)


class DateTimeRule(Rule):
    """
    Valid date/time matching the default 'YYYY-MM-DD hh:mm:ss' format, or a
    custom specified format.
    """

    name = "date_time"
    stop = True
    default_format = config.DEFAULT_DATE_TIME_FORMAT

    _regex = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        supplied_format = parameters[0] if parameters else None
        _date_time_format = supplied_format or DateTimeRule.default_format
        self.message_fields = dict(field=field, format=_date_time_format)

        return self.valid_date_time(value, supplied_format)

    @property
    def message(self) -> str:
        return errors.DATE_TIME_ERROR

    @staticmethod
    def valid_date_time(value: Any, date_time_format: str = None) -> bool:
        if isinstance(value, datetime):
            return True

        if not date_time_format and not regex_match(DateTimeRule._regex, value):
            return False

        try:
            datetime.strptime(value, date_time_format or DateTimeRule.default_format)
        except (ValueError, TypeError):
            return False

        return True


class BeforeRule(Rule):
    """Date/time that must occur before another date/time."""

    name = "before"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        supplied_field_or_format = parameters[0] if parameters else None
        before_date, before_format = self.date_and_format(field, field, validator)
        after_date, after_format = self.date_and_format(
            field, supplied_field_or_format, validator
        )
        self.message_fields = dict(field=field, other=supplied_field_or_format)

        return before_date < after_date

    @staticmethod
    def date_and_format(
        field: str, field_or_date_time: Any, validator
    ) -> Tuple[datetime, str]:
        after_format = DateTimeRule.default_format

        # First try the value as a datetime string with the default format. If
        # it fails, try and find out if a datetime format has been specified in
        # the rule set.
        try:
            after_date = datetime.strptime(field_or_date_time, after_format)
        except (ValueError, TypeError):
            after_format = BeforeRule.date_time_field_format(
                field_or_date_time, validator
            )
            value = get_field_value(data=validator.data, field=field_or_date_time or "")

            if isinstance(value, datetime):
                after_date = value
            else:
                try:
                    after_date = datetime.strptime(value, after_format)
                except (ValueError, TypeError):
                    after_format = BeforeRule.date_time_field_format(field, validator)
                    try:
                        after_date = datetime.strptime(field_or_date_time, after_format)
                    except (ValueError, TypeError):
                        raise InvalidDateTimeFormat

        return after_date, after_format

    @staticmethod
    def date_time_field_format(field, validator) -> str:
        date_time_format = None
        if field in validator.rules:
            rules = validator.field_rules(field)
            for rule, parameters in validator.rule_iterator(rules):
                if rule.name == DateTimeRule.name and parameters:
                    date_time_format = parameters[0]

        return date_time_format or DateTimeRule.default_format

    @property
    def message(self) -> str:
        return errors.BEFORE_ERROR


class BeforeOrEqualRule(BeforeRule):
    """Date/time that must be before or equal to another date/time."""

    name = "before_or_equal"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        supplied_field_or_format = parameters[0] if parameters else None
        before_or_equal_date, before_or_equal_format = self.date_and_format(
            field, field, validator
        )
        after_or_equal_date, after_or_equal_format = self.date_and_format(
            field, supplied_field_or_format, validator
        )
        self.message_fields = dict(field=field, other=supplied_field_or_format)

        return before_or_equal_date <= after_or_equal_date

    @property
    def message(self) -> str:
        return errors.BEFORE_OR_EQUAL_ERROR


class AfterRule(Rule):
    """Date/time that must occur after another date/time."""

    name = "after"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        supplied_field_or_format = parameters[0] if parameters else None
        after_date, after_format = BeforeRule.date_and_format(field, field, validator)
        before_date, before_format = BeforeRule.date_and_format(
            field, supplied_field_or_format, validator
        )
        self.message_fields = dict(field=field, other=supplied_field_or_format)

        return after_date > before_date

    @property
    def message(self) -> str:
        return errors.AFTER_ERROR


class AfterOrEqualRule(AfterRule):
    """Date/time that must be after or equal to another date/time."""

    name = "after_or_equal"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        supplied_field_or_format = parameters[0] if parameters else None
        after_or_equal_date, after_or_equal_format = BeforeRule.date_and_format(
            field, field, validator
        )
        before_or_equal_date, before_or_equal_format = BeforeRule.date_and_format(
            field, supplied_field_or_format, validator
        )
        self.message_fields = dict(field=field, other=supplied_field_or_format)

        return after_or_equal_date >= before_or_equal_date

    @property
    def message(self) -> str:
        return errors.AFTER_OR_EQUAL_ERROR


class SizeRule(Rule):
    """Size"""

    name = "size"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        size = parameters[0]
        self.message_fields = dict(field=field, size=size)
        expected = float(size)

        if isinstance(value, str):
            return len(value) == expected
        elif isinstance(value, list) or isinstance(value, dict):
            return len(value) == expected
        elif isinstance(value, int):
            return value == expected
        elif isinstance(value, float):
            return value == expected
        elif isinstance(value, Decimal):
            expected = Decimal(size)
            return value == expected

        return False

    @property
    def message(self) -> str:
        return errors.SIZE_ERROR


class EndsWithRule(Rule):
    """The field under validation must end with one of the given values."""

    name = "ends_with"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self.message_fields = dict(field=field, values=parameters)

        return any([str(value).endswith(rule_val) for rule_val in parameters])

    @property
    def message(self) -> str:
        return errors.ENDS_WITH_ERROR


class RegexRule(Rule):
    """The field under validation must match the regex."""

    name = "regex"

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        regex = parameters[0]
        self.message_fields = dict(field=field, regex=regex)
        regex = re.compile(regex)

        return regex_match(regex, value)

    @property
    def message(self) -> str:
        return errors.REGEX_ERROR


class _FunctionRule(Rule):
    """The field under validation must pass the supplied function."""

    def __init__(self, validation_function):
        super().__init__()
        self._result = None
        self.validation_function = validation_function

    def passes(self, field: str, value: Any, parameters: List[str], validator) -> bool:
        self._result = self.validation_function(
            field=field, value=value, validator=validator
        )
        self.message_fields = dict(field=field)

        return self._result is None

    @property
    def message(self) -> str:
        return self._result

    @property
    def name(self):
        return self.__class__.__name__
