import ipaddress
from uuid import UUID
from abc import ABC, abstractmethod

from spotlight import errors
from spotlight.utils import missing, equals, empty, regex_match


class BaseRule(ABC):
    def __init__(self):
        self.name = None
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


class InputDependentRule(BaseRule):
    @abstractmethod
    def passes(self, field, value, input_) -> bool:
        pass


class DependentRule(BaseRule):
    @abstractmethod
    def passes(self, field, values, input_) -> bool:
        pass


class DependentSessionRule(DependentRule):
    def __init__(self, session):
        super().__init__()
        self._session = session

    @abstractmethod
    def passes(self, field, values, input_) -> bool:
        pass


class UppercaseRule(Rule):
    def __init__(self):
        super().__init__()
        self.name = "uppercase"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return value.upper() == value

    def message(self) -> str:
        return "The {field} field must be uppercase."


class RequiredRule(InputDependentRule):
    """Required field"""
    def __init__(self):
        super().__init__()
        self.name = "required"
        self.implicit = True
        self.stop = True

    def passes(self, field, value, input_) -> bool:
        self.message_fields = dict(field=field)

        return not missing(input_, field) and not empty(value)

    def message(self) -> str:
        return errors.REQUIRED_ERROR


class RequiredWithoutRule(DependentRule):
    """Required if other field is not present"""
    def __init__(self):
        super().__init__()
        self.name = "required_without"
        self.implicit = True
        self.stop = True

    def passes(self, field, values, input_) -> bool:
        other = values[0]
        self.message_fields = dict(field=field, other=other)

        return not missing(input_, field) and missing(input_, other)

    def message(self) -> str:
        return errors.REQUIRED_WITHOUT_ERROR


class RequiredWithRule(DependentRule):
    """Required with other field"""
    def __init__(self):
        super().__init__()
        self.name = "required_with"
        self.implicit = True
        self.stop = True

    def passes(self, field, values, input_) -> bool:
        other = values[0]
        self.message_fields = dict(
            field=field,
            other=other
        )

        if missing(input_, field) and input_.get(other):
            return False

        return True

    def message(self) -> str:
        return errors.REQUIRED_WITH_ERROR


class RequiredIfRule(DependentRule):
    """Required if other field equals certain value"""
    def __init__(self):
        super().__init__()
        self.name = "required_if"
        self.implicit = True
        self.stop = True

    def passes(self, field, values, input_) -> bool:
        other, val = values[0].split(",")
        other_val = input_.get(other)
        self.message_fields = dict(
            field=field,
            other=other,
            value=val
        )

        if missing(input_, field) and equals(val, other_val):
            return False

        return True

    def message(self) -> str:
        return errors.REQUIRED_IF_ERROR


class NotWithRule(DependentRule):
    """Not with other field"""
    def __init__(self):
        super().__init__()
        self.name = "not_with"
        self.stop = True

    def passes(self, field, values, input_) -> bool:
        other = values[0]
        self.message_fields = dict(
            field=field,
            other=other
        )

        if not missing(input_, field) and not missing(input_, other):
            return False

        return True

    def message(self) -> str:
        return errors.NOT_WITH_ERROR


class FilledRule(InputDependentRule):
    """Not empty when present"""
    def __init__(self):
        super().__init__()
        self.name = "filled"
        self.implicit = True
        self.stop = True

    def passes(self, field, value, input_) -> bool:
        self.message_fields = dict(field=field)

        if field in input_ and empty(value):
            return False

        return True

    def message(self) -> str:
        return errors.FILLED_ERROR


class EmailRule(Rule):
    """Valid email"""
    def __init__(self):
        super().__init__()
        self.name = "email"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_email(value)

    def message(self) -> str:
        return errors.INVALID_EMAIL_ERROR

    @staticmethod
    def valid_email(email):
        return regex_match(
            r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",
            email
        )


class UrlRule(Rule):
    """Valid URL"""
    def __init__(self):
        super().__init__()
        self.name = "url"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_url(value)

    def message(self) -> str:
        return errors.INVALID_URL_ERROR

    @staticmethod
    def valid_url(url):
        if not StringRule.valid_string(url):
            return False

        return url.startswith("http://") or url.startswith("https://")


class IpRule(Rule):
    """Valid IP"""
    def __init__(self):
        super().__init__()
        self.name = "ip"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_ip(value)

    def message(self) -> str:
        return errors.INVALID_IP_ERROR

    @staticmethod
    def valid_ip(ip):
        if not StringRule.valid_string(ip) and not IntegerRule.valid_integer(ip):
            return False
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False


class MinRule(DependentRule):
    """Min length"""
    def __init__(self):
        super().__init__()
        self.name = "min"

    def passes(self, field, values, input_) -> bool:
        _min = int(values[0])
        value = input_.get(field)
        self.message_fields = dict(field=field, min=_min)

        if StringRule.valid_string(value) or type(value) is list:
            return len(value) >= _min
        elif IntegerRule.valid_integer(value):
            return value >= _min

        return False

    def message(self) -> str:
        return errors.MIN_ERROR


class MaxRule(DependentRule):
    """Max length"""
    def __init__(self):
        super().__init__()
        self.name = "max"

    def passes(self, field, values, input_) -> bool:
        _max = int(values[0])
        value = input_.get(field)
        self.message_fields = dict(field=field, max=_max)

        if StringRule.valid_string(value) or type(value) is list:
            return len(value) <= _max
        elif IntegerRule.valid_integer(value):
            return value <= _max

        return False

    def message(self) -> str:
        return errors.MAX_ERROR


class InRule(DependentRule):
    """
        In: The field under validation must be included in the given list
        of values
    """
    def __init__(self):
        super().__init__()
        self.name = "in"

    def passes(self, field, values, input_) -> bool:
        _values = values[0].split(",")
        self.message_fields = dict(field=field, values=", ".join(_values))

        return input_.get(field) in _values

    def message(self) -> str:
        return errors.IN_ERROR


class AlphaNumRule(Rule):
    """Only letters and numbers"""
    def __init__(self):
        super().__init__()
        self.name = "alpha_num"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num(value)

    def message(self) -> str:
        return errors.ALPHA_NUM_ERROR

    @staticmethod
    def valid_alpha_num(value):
        return regex_match(r"^[a-zA-Z0-9]+$", value)


class AlphaNumSpaceRule(Rule):
    """Only letters, numbers and spaces"""
    def __init__(self):
        super().__init__()
        self.name = "alpha_num_space"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_alpha_num_space(value)

    def message(self) -> str:
        return errors.ALPHA_NUM_SPACE_ERROR

    @staticmethod
    def valid_alpha_num_space(value):
        return regex_match(r"^[a-zA-Z0-9 ]+$", value)


class StringRule(Rule):
    """Valid string"""
    def __init__(self):
        super().__init__()
        self.name = "string"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_string(value)

    def message(self) -> str:
        return errors.STRING_ERROR

    @staticmethod
    def valid_string(string):
        return type(string) is str


class IntegerRule(Rule):
    """Valid integer"""
    def __init__(self):
        super().__init__()
        self.name = "integer"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_integer(value)

    def message(self) -> str:
        return errors.INTEGER_ERROR

    @staticmethod
    def valid_integer(integer):
        return type(integer) is int


class BooleanRule(Rule):
    """Valid boolean"""
    def __init__(self):
        super().__init__()
        self.name = "boolean"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_boolean(value)

    def message(self) -> str:
        return errors.BOOLEAN_ERROR

    @staticmethod
    def valid_boolean(boolean):
        return type(boolean) is bool


class Uuid4Rule(Rule):
    """Valid uuid4"""
    def __init__(self):
        super().__init__()
        self.name = "uuid4"

    def passes(self, field, value) -> bool:
        self.message_fields = dict(field=field)

        return self.valid_uuid4(value)

    def message(self) -> str:
        return errors.UUID4_ERROR

    @staticmethod
    def valid_uuid4(uuid):
        if type(uuid) is UUID:
            uuid = str(uuid)
        try:
            val = UUID(uuid, version=4)
        except:
            return False

        return str(val) == uuid


class UniqueRule(DependentSessionRule):
    """Unique database record"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "unique"

    def passes(self, field, values, input_) -> bool:
        self.message_fields = dict(field=field)
        table, column, *extra = values[0].split(",")

        ignore_col = extra[0] if len(extra) > 0 else None
        ignore_val = extra[1] if len(extra) > 1 else None
        where_col = extra[2] if len(extra) > 2 else None
        where_val = extra[3] if len(extra) > 3 else None

        exists = self._unique_check(
            input_,
            table,
            column,
            ignore_col,
            ignore_val,
            where_col,
            where_val
        )

        return not exists

    def message(self) -> str:
        return errors.UNIQUE_ERROR

    def _unique_check(
        self,
        input_,
        table,
        column,
        ignore_col=None,
        ignore_val=None,
        where_col=None,
        where_val=None
    ):
        # Create query
        query = "SELECT * FROM {} WHERE {} = :value1".format(table, column)
        params = {
            "value1": input_.get(column)
        }

        # If ignore values are set
        if (ignore_col and ignore_val and ignore_col != "null" and
                ignore_val != "null"):
            query += " AND {} != :ignore_val".format(ignore_col)
            params["ignore_val"] = ignore_val

        # If where values are set
        if where_col and where_val:
            query += " AND {} = :where_val".format(where_col)
            params["where_val"] = where_val

        result = self._session.execute(query, params).first()

        return result


class ExistsRule(DependentSessionRule):
    """Exists in database"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "exists"
        self.error = None

    def passes(self, field, values, input_) -> bool:
        table, column, *extra = values[0].split(",")

        # Check if extra where is set
        if extra:
            where_col = extra[0]
            where_val = extra[1]
            self.message_fields = dict(field=field, other=where_col)
            self.error = errors.EXISTS_WHERE_ERROR

            query = (
                "SELECT * FROM {} WHERE {} = :value1 "
                "AND {} = :value2".format(table, column, where_col)
            )
            params = {
                "value1": input_.get(field),
                "value2": where_val
            }
            exists = self._session.execute(query, params).first()
        else:
            self.message_fields = dict(field=field)
            self.error = errors.EXISTS_ERROR

            query = "SELECT * FROM {} WHERE {} = :value1".format(
                table,
                column
            )
            params = {
                "value1": input_.get(field)
            }
            exists = self._session.execute(query, params).first()

        return exists

    def message(self) -> str:
        return self.error
