import ipaddress
import json
import re
from typing import Any
from uuid import UUID
from abc import ABC, abstractmethod

from spotlight import errors
from spotlight.exceptions import RuleNameAlreadyExistsError, AttributeNotImplementedError
from spotlight.utils import missing, equals, empty, regex_match


class Rule(ABC):
    name = NotImplemented
    implicit = False
    stop = False

    subclasses = []

    def __init__(self):
        self.message_fields = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # if Rule in cls.__bases__:
        #     return
        if cls.name is NotImplemented:
            raise AttributeNotImplementedError("name", cls.__name__)
        if cls.name in [subclass.name for subclass in cls.subclasses]:
            raise RuleNameAlreadyExistsError(cls.name)

        cls.subclasses.append(cls)

    @abstractmethod
    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError

    # @overload
    # @abstractmethod
    # def test(self, field: str, value: str) -> bool:
    #     ...
    #
    # @overload
    # @abstractmethod
    # def test(self, field: str, value: str, rule_values: list, input_: dict) -> bool:
    #     ...
    #
    # @abstractmethod
    # def test(self, *args, **kwargs) -> bool:
    #     raise NotImplementedError


# class RuleOld(BaseRule):
#     @abstractmethod
#     def passes(self, field: str, value: Any) -> bool:
#         pass
#
#
# class DependentRule(BaseRule):
#     @abstractmethod
#     def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
#         pass


class RequiredRule(Rule):
    """Required field"""

    name = "required"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return not missing(input_, field) and not empty(value)

    @property
    def message(self) -> str:
        return errors.REQUIRED_ERROR


class RequiredWithoutRule(Rule):
    """Required if other field is not present"""

    name = "required_without"
    implicit = True
    stop = True

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        other_fields = rule_values.split(",")
        self.message_fields = dict(field=field, other=", ".join(other_fields))

        if missing(input_, field) and any(missing(input_, o) for o in other_fields):
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

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        other_fields = rule_values.split(",")
        self.message_fields = dict(field=field, other=", ".join(other_fields))

        if missing(input_, field) and any(not missing(input_, o) for o in other_fields):
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

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        other, val = rule_values.split(",")
        other_val = input_.get(other)
        self.message_fields = dict(field=field, other=other, value=val)

        if missing(input_, field) and equals(val, other_val):
            return False

        return True

    @property
    def message(self) -> str:
        return errors.REQUIRED_IF_ERROR


class NotWithRule(Rule):
    """Not with other field"""

    name = "not_with"
    stop = True

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        other = rule_values
        self.message_fields = dict(field=field, other=other)

        if not missing(input_, field) and not missing(input_, other):
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

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)
        if self._field_in_input(field, input_) and empty(value):
            return False

        return True

    @staticmethod
    def _field_in_input(field, input_) -> bool:
        value = input_
        split_field = field.split(".")
        try:
            for key in split_field:
                value = value[key]
        except KeyError:
            return False

        return True

    @property
    def message(self) -> str:
        return errors.FILLED_ERROR


class EmailRule(Rule):
    """Valid email"""

    name = "email"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_email(value)

    @property
    def message(self) -> str:
        return errors.INVALID_EMAIL_ERROR

    @staticmethod
    def valid_email(email) -> bool:
        return regex_match(
            r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",
            email,
        )


class UrlRule(Rule):
    """Valid URL"""

    name = "url"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_url(value)

    @property
    def message(self) -> str:
        return errors.INVALID_URL_ERROR

    @staticmethod
    def valid_url(url) -> bool:
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return regex_match(regex, url)


class IpRule(Rule):
    """Valid IP"""

    name = "ip"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_ip(value)

    @property
    def message(self) -> str:
        return errors.INVALID_IP_ERROR

    @staticmethod
    def valid_ip(ip) -> bool:
        if not StringRule.valid_string(ip) and not IntegerRule.valid_integer(ip):
            return False
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False


class MinRule(Rule):
    """Min length"""

    name = "min"

    def __init__(self):
        super().__init__()
        self.error = None

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        min_ = rule_values
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

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        max_ = rule_values
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

        return False

    @property
    def message(self) -> str:
        return self.error


class InRule(Rule):
    """
        In: The field under validation must be included in the given list
        of values
    """

    name = "in"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        _rule_values = rule_values.split(",")
        self.message_fields = dict(field=field, values=", ".join(_rule_values))

        return str(value) in _rule_values

    @property
    def message(self) -> str:
        return errors.IN_ERROR


class AlphaNumRule(Rule):
    """Only letters and numbers"""

    name = "alpha_num"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num(value)

    @property
    def message(self) -> str:
        return errors.ALPHA_NUM_ERROR

    @staticmethod
    def valid_alpha_num(value) -> bool:
        return regex_match(r"^[a-zA-Z0-9]+$", value)


class AlphaNumSpaceRule(Rule):
    """Only letters, numbers and spaces"""

    name = "alpha_num_space"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num_space(value)

    @property
    def message(self) -> str:
        return errors.ALPHA_NUM_SPACE_ERROR

    @staticmethod
    def valid_alpha_num_space(value) -> bool:
        return regex_match(r"^[a-zA-Z0-9 ]+$", value)


class StringRule(Rule):
    """Valid string"""

    name = "string"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_string(value)

    @property
    def message(self) -> str:
        return errors.STRING_ERROR

    @staticmethod
    def valid_string(string) -> bool:
        return type(string) is str


class IntegerRule(Rule):
    """Valid integer"""

    name = "integer"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_integer(value)

    @property
    def message(self) -> str:
        return errors.INTEGER_ERROR

    @staticmethod
    def valid_integer(integer) -> bool:
        return type(integer) is int


class FloatRule(Rule):
    """Valid float"""

    name = "float"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_float(value)

    @property
    def message(self) -> str:
        return errors.FLOAT_ERROR

    @staticmethod
    def valid_float(float_) -> bool:
        return type(float_) is float


class BooleanRule(Rule):
    """Valid boolean"""

    name = "boolean"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_boolean(value)

    @property
    def message(self) -> str:
        return errors.BOOLEAN_ERROR

    @staticmethod
    def valid_boolean(boolean) -> bool:
        return type(boolean) is bool


class ListRule(Rule):
    """Valid list"""

    name = "list"
    stop = True

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_list(value)

    @property
    def message(self) -> str:
        return errors.LIST_ERROR

    @staticmethod
    def valid_list(value) -> bool:
        return type(value) is list


class Uuid4Rule(Rule):
    """Valid uuid4"""

    name = "uuid4"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_uuid4(value)

    @property
    def message(self) -> str:
        return errors.UUID4_ERROR

    @staticmethod
    def valid_uuid4(uuid) -> bool:
        if type(uuid) is UUID:
            uuid = str(uuid)
        try:
            val = UUID(uuid, version=4)
        except:
            return False

        return str(val) == uuid


class JsonRule(Rule):
    """Valid json"""

    name = "json"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
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
        except:
            return False


class AcceptedRule(Rule):
    """The field must be yes, on, 1, or true"""

    name = "accepted"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        accepted_values = ["yes", "on", 1, True]
        self.message_fields = dict(field=field)

        return value in accepted_values

    @property
    def message(self) -> str:
        return errors.ACCEPTED_ERROR


class StartsWithRule(Rule):
    """The field under validation must start with one of the given values."""

    name = "starts_with"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        _rule_values = rule_values.split(",")
        self.message_fields = dict(field=field, values=", ".join(_rule_values))

        return any([str(value).startswith(rule_val) for rule_val in _rule_values])

    @property
    def message(self) -> str:
        return errors.STARTS_WITH_ERROR


class DictRule(Rule):
    """Valid dict"""

    name = "dict"

    def passes(self, field: str, value: Any, rule_values: str, input_: dict) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_dict(value)

    @property
    def message(self) -> str:
        return errors.DICT_ERROR

    @staticmethod
    def valid_dict(value) -> bool:
        return type(value) is dict
