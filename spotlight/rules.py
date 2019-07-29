import ipaddress
import json
import re
from uuid import UUID
from abc import ABC, abstractmethod

from spotlight import errors
from spotlight.utils import missing, equals, empty, regex_match


class BaseRule(ABC):
    name = None

    def __init__(self):
        self.implicit = False
        self.stop = False
        self.message_fields = {}

    @abstractmethod
    def message(self) -> str:
        pass


class Rule(BaseRule):
    @abstractmethod
    def passes(self, field, value) -> bool:
        pass


class DependentRule(BaseRule):
    @abstractmethod
    def passes(self, field, value, rule_values, input_) -> bool:
        pass


class RequiredRule(DependentRule):
    """Required field"""

    name = "required"

    def __init__(self):
        super().__init__()
        self.implicit = True
        self.stop = True

    def passes(self, field, value, rule_values, input_) -> bool:
        self.message_fields = dict(field=field)

        return not missing(input_, field) and not empty(value)

    def message(self) -> str:
        return errors.REQUIRED_ERROR


class RequiredWithoutRule(DependentRule):
    """Required if other field is not present"""

    name = "required_without"

    def __init__(self):
        super().__init__()
        self.implicit = True
        self.stop = True

    def passes(self, field, value, rule_values, input_) -> bool:
        other = rule_values[0]
        self.message_fields = dict(field=field, other=other)

        return not missing(input_, field) and missing(input_, other)

    def message(self) -> str:
        return errors.REQUIRED_WITHOUT_ERROR


class RequiredWithRule(DependentRule):
    """Required with other field"""

    name = "required_with"

    def __init__(self):
        super().__init__()
        self.implicit = True
        self.stop = True

    def passes(self, field, value, rule_values, input_) -> bool:
        other = rule_values[0]
        self.message_fields = dict(field=field, other=other)

        if missing(input_, field) and input_.get(other):
            return False

        return True

    def message(self) -> str:
        return errors.REQUIRED_WITH_ERROR


class RequiredIfRule(DependentRule):
    """Required if other field equals certain value"""

    name = "required_if"

    def __init__(self):
        super().__init__()
        self.implicit = True
        self.stop = True

    def passes(self, field, value, rule_values, input_) -> bool:
        other, val = rule_values[0].split(",")
        other_val = input_.get(other)
        self.message_fields = dict(field=field, other=other, value=val)

        if missing(input_, field) and equals(val, other_val):
            return False

        return True

    def message(self) -> str:
        return errors.REQUIRED_IF_ERROR


class NotWithRule(DependentRule):
    """Not with other field"""

    name = "not_with"

    def __init__(self):
        super().__init__()
        self.stop = True

    def passes(self, field, value, rule_values, input_) -> bool:
        other = rule_values[0]
        self.message_fields = dict(field=field, other=other)

        if not missing(input_, field) and not missing(input_, other):
            return False

        return True

    def message(self) -> str:
        return errors.NOT_WITH_ERROR


def field_in_input(field, input_):
    value = input_
    split_field = field.split(".")
    try:
        for key in split_field:
            value = value[key]
    except KeyError:
        return False

    return True


class FilledRule(DependentRule):
    """Not empty when present"""

    name = "filled"

    def __init__(self):
        super().__init__()
        self.implicit = True
        self.stop = True

    def passes(self, field, value, rule_values, input_) -> bool:
        self.message_fields = dict(field=field)
        if field_in_input(field, input_) and empty(value):
            return False

        return True

    def message(self) -> str:
        return errors.FILLED_ERROR


class EmailRule(Rule):
    """Valid email"""

    name = "email"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_email(value)

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

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_url(value)

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

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_ip(value)

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


class MinRule(DependentRule):
    """Min length"""

    name = "min"

    def __init__(self):
        super().__init__()
        self.error = None

    def passes(self, field, value, rule_values, input_) -> bool:
        _min = rule_values[0]
        self.message_fields = dict(field=field, min=_min)
        self.error = errors.MIN_ERROR

        if StringRule.valid_string(value):
            self.error = errors.MIN_STRING_ERROR
            return len(value) >= int(_min)
        elif type(value) is list:
            self.error = errors.MIN_LIST_ERROR
            return len(value) >= int(_min)
        elif IntegerRule.valid_integer(value):
            return value >= int(_min)
        elif FloatRule.valid_float(value):
            return value >= float(_min)

        return False

    def message(self) -> str:
        return self.error


class MaxRule(DependentRule):
    """Max length"""

    name = "max"

    def __init__(self):
        super().__init__()
        self.error = None

    def passes(self, field, value, rule_values, input_) -> bool:
        _max = rule_values[0]
        self.message_fields = dict(field=field, max=_max)
        self.error = errors.MAX_ERROR

        if StringRule.valid_string(value):
            self.error = errors.MAX_STRING_ERROR
            return len(value) <= int(_max)
        elif type(value) is list:
            self.error = errors.MAX_LIST_ERROR
            return len(value) <= int(_max)
        elif IntegerRule.valid_integer(value):
            return value <= int(_max)
        elif FloatRule.valid_float(value):
            return value <= float(_max)

        return False

    def message(self) -> str:
        return self.error


class InRule(DependentRule):
    """
        In: The field under validation must be included in the given list
        of values
    """

    name = "in"

    def passes(self, field, value, rule_values, input_) -> bool:
        _rule_values = rule_values[0].split(",")
        self.message_fields = dict(field=field, values=", ".join(_rule_values))

        return str(value).lower() in _rule_values

    def message(self) -> str:
        return errors.IN_ERROR


class AlphaNumRule(Rule):
    """Only letters and numbers"""

    name = "alpha_num"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num(value)

    def message(self) -> str:
        return errors.ALPHA_NUM_ERROR

    @staticmethod
    def valid_alpha_num(value) -> bool:
        return regex_match(r"^[a-zA-Z0-9]+$", value)


class AlphaNumSpaceRule(Rule):
    """Only letters, numbers and spaces"""

    name = "alpha_num_space"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num_space(value)

    def message(self) -> str:
        return errors.ALPHA_NUM_SPACE_ERROR

    @staticmethod
    def valid_alpha_num_space(value) -> bool:
        return regex_match(r"^[a-zA-Z0-9 ]+$", value)


class StringRule(Rule):
    """Valid string"""

    name = "string"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_string(value)

    def message(self) -> str:
        return errors.STRING_ERROR

    @staticmethod
    def valid_string(string) -> bool:
        return type(string) is str


class IntegerRule(Rule):
    """Valid integer"""

    name = "integer"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_integer(value)

    def message(self) -> str:
        return errors.INTEGER_ERROR

    @staticmethod
    def valid_integer(integer) -> bool:
        return type(integer) is int


class FloatRule(Rule):
    """Valid float"""

    name = "float"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_float(value)

    def message(self) -> str:
        return errors.FLOAT_ERROR

    @staticmethod
    def valid_float(float_) -> bool:
        return type(float_) is float


class BooleanRule(Rule):
    """Valid boolean"""

    name = "boolean"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_boolean(value)

    def message(self) -> str:
        return errors.BOOLEAN_ERROR

    @staticmethod
    def valid_boolean(boolean) -> bool:
        return type(boolean) is bool


class ListRule(Rule):
    """Valid list"""

    name = "list"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_list(value)

    def message(self) -> str:
        return errors.LIST_ERROR

    @staticmethod
    def valid_list(value) -> bool:
        return type(value) is list


class Uuid4Rule(Rule):
    """Valid uuid4"""

    name = "uuid4"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_uuid4(value)

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

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_json(value)

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

    def passes(self, field, value) -> bool:
        accepted_values = ["yes", "on", 1, True]
        self.message_fields = dict(field=field)

        return value in accepted_values

    def message(self) -> str:
        return errors.ACCEPTED_ERROR


class StartsWithRule(DependentRule):
    """The field under validation must start with one of the given values."""

    name = "starts_with"

    def passes(self, field, value, rule_values, input_) -> bool:
        _rule_values = rule_values[0].split(",")
        self.message_fields = dict(field=field, values=", ".join(_rule_values))

        valid = False
        for rule_val in _rule_values:
            if str(value).startswith(rule_val):
                valid = True

        return valid

    def message(self) -> str:
        return errors.STARTS_WITH_ERROR


class DictRule(Rule):
    """Valid dict"""

    name = "dict"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_dict(value)

    def message(self) -> str:
        return errors.DICT_ERROR

    @staticmethod
    def valid_dict(value) -> bool:
        return type(value) is dict
